import copy
import random as rd
from datetime import timedelta, datetime
from sys import stderr
from collections import deque
from .event import EVENT_TYPE, Confirm_task, WorkTimeDelay, Temp_need, Canceled, Start_work, End_work, Deny_and_confirm
from .model import SHIP, TASK, TUG, CHARGE_TYPE, TUG_STATE, TASK_STATE
from .scheduler import Scheduler
from .settings import TUG_SPEED, set_system_time, get_system_time
from .data_reading import df_pier_to_pier
from .utils.utility import count_move_time, max_arrival_time, find_required_tug, gen_delay_time
from .predict_worktime import predict_worktime

def gen_tempNeed(tasks, tugs, probability):
    queue = []
    for task in tasks:
        # decide whether tempNeed event will happen
        dice = rd.uniform(0, 1)
        # Only if original need of tug is less than 3, add tug event will happen
        if dice > probability or task.tug_cnt >= 3:
            continue

        extra_tug = []
        task_tug_id = set([i.tug_id for i in task.tugs])
        
        idx = 0
        # Only allowed to add one tug and random add tug is not allowed to be the same tug that assign to this task
        while not extra_tug or extra_tug[0].tug_id in task_tug_id:
            extra_tug = []
            extra_tug.append(sorted(tugs, key=lambda x: x.next_available_time)[idx])
            idx += 1

        time = task.start_time+timedelta(minutes=0.55)
        queue.append(Temp_need(task, extra_tug, tugs, tasks,
        max(get_system_time(), time)))

    return (queue)

# generate confirm event
def gen_match(task, tugs, ships, tasks):  
    event = Confirm_task(task, tugs, ships, tasks, 
                        max(task.start_time, max_arrival_time(task, task.tugs)) -
                        timedelta(minutes=10))
    return (event)

# generate deny and confirm event
def gen_deny_and_confirm(task, tasks, tugs):
    addOrChanged = rd.randint(0, 1)
    if addOrChanged == 0 or task.tug_cnt >= 3:
        required_tugs_list = find_required_tug(task.ship.weight, task.tug_cnt)
        # the number of tugs is to be changed
        change_cnt = rd.randint(1, len(required_tugs_list))
        temp_need_tug = copy.deepcopy(task.tugs)
        # shuffle the tug to be random
        rd.shuffle(tugs)
        for tug in tugs:
            # counting the move time
            move_time = count_move_time(
                task.ship_state, tug.pos, task.start)  
            # when task start, the tug is available and can arrived at time
            if tug.next_available_time + move_time <= task.start_time:
                for i in range(change_cnt):
                    # choose the tug whose horse power is higher
                    if tug.type > required_tugs_list[i]:
                        temp_need_tug[i] = tug
                        break

        # sort the temp_need_tug to conform to the dispathing algorithm
        temp_need_tug.sort(key=lambda x: x.type)
        time = max(task.start_time, max_arrival_time(
            task, temp_need_tug)) - timedelta(minutes=10)
        event = Deny_and_confirm(
            task, temp_need_tug, tugs, tasks, max(get_system_time(), time))
        return (event)

    else:
        if task.tug_cnt < 3:  # 本來派三拖內才可以加船
            temp_need_tug = copy.deepcopy(task.tugs)
            extra_tug = []
            for tug in tugs:
                if tug.state == TUG_STATE.FREE:
                    extra_tug.append(tug)
            random_num = rd.randint(0, len(extra_tug) - 1)
            extra_tug = extra_tug[random_num]

        temp_need_tug.append(extra_tug)
        temp_need_tug.sort(key=lambda x: x.type)
        time = max(task.start_time, max_arrival_time(
            task, temp_need_tug)) - timedelta(minutes=10)
        event = Deny_and_confirm(
            task, temp_need_tug, tugs, tasks, max(get_system_time(), time))
        return(event)


def gen_confirm(unconfirmed_tasks, tugs, tasks, ships, confirmed_prob):
    queue = []
    for task in unconfirmed_tasks:
        # confirm the task with tugs have been assigned
        dice = rd.uniform(0, 1)
        if dice <= confirmed_prob:
            queue.append(gen_match(task, tugs, ships, tasks))
        else:
            queue.append(gen_deny_and_confirm(task, tasks, tugs))
    return (queue)

def gen_workTimeDelay(unconfirmed_tasks, tugs, probability):  
    queue = []
    for task in unconfirmed_tasks:
        delay_time = gen_delay_time(task)
        true_start_time = task.start_time
        move_time = timedelta(minutes=0)
        for tug in task.tugs:
            if true_start_time < tug.next_available_time:
                true_start_time = tug.next_available_time

            move_time = max(move_time, count_move_time(
                task.task_state, tug.pos, task.start, TUG_SPEED))

        time = true_start_time + timedelta(minutes=0.5)
        temp = WorkTimeDelay(task=task, delay_time=delay_time,
                            task_list=unconfirmed_tasks, time=time, tug_list=tugs)
        queue.append(temp)
    return(queue)


def gen_workStartAndEnd(unconfirmed_tasks, total_tasks, tugs, tasks, ships):
    queue = []
    for task in unconfirmed_tasks:
        true_start_time = task.start_time
        move_time = timedelta(minutes=0)
        for tug in task.tugs:
            if true_start_time < tug.next_available_time:
                true_start_time = tug.next_available_time
            move_time = max(move_time, count_move_time(
                task.task_state, tug.pos, task.start, TUG_SPEED))
        queue.append(Start_work(task, tasks, tugs, ships, time=max(
            get_system_time(), true_start_time - timedelta(minutes=0.1))))
        queue.append(End_work(task,tugs, tasks,total_tasks, ships,
                            time=true_start_time + task.work_time))
    return (queue)


def gen_canceled(unconfirmed_tasks, tugs, probability):
    queue = []
    for task in unconfirmed_tasks:
        dice = rd.uniform(0, 1)
        if dice > probability:
            continue
        queue.append(Canceled(task, unconfirmed_tasks,
            time=task.start_time - timedelta(minutes=1)))
    return (queue)

class Simulator():
    def update_tasks(self):
        self.tasks = [task for task in self.total_tasks \
            if task.start_time - get_system_time() <= timedelta(minutes=30)]
        
    def __init__(self, events, total_tasks, tugs, ships, method):
        self.method = method
        self.total_tasks = total_tasks
        self.tasks = []
        self.update_tasks()
        self.tugs = tugs
        self.scheduler = Scheduler(self.method)
        self.ships = ships

        unconfirmed_tasks = self.scheduler.method(self.tasks, self.tugs)
        unconfirmed_tasks = [ \
            i for i in unconfirmed_tasks if i.task_state == TASK_STATE.UNPROCESSED_ASSIGNED]

        self.events = self.gen_event(unconfirmed_tasks, 
                    self.total_tasks, self.tasks, self.tugs, self.ships)

    def run(self):
        self.events.sort(key=lambda x: x.time)

        while self.events:
            # set the system time
            event = self.events.pop(0)
            set_system_time(event.time)
            print(event, file=stderr)
            # deal with (temp need before worktime delay)
            event.handle()
            
            
            
            if event.type == EVENT_TYPE.WORK_TIME_DELAY or \
                    event.type == EVENT_TYPE.CANCELED or \
                    event.type == EVENT_TYPE.TEMP_NEED or \
                    event.type == EVENT_TYPE.DENY_AND_CONFIRM or \
                    event.type == EVENT_TYPE.END_WORK:
                
                
                # update the task
                tasks_ids = set([task.id for task in self.tasks])
                self.tasks = self.tasks + [task for task in self.total_tasks if task.id not in tasks_ids and task.start_time - get_system_time() <= timedelta(minutes=30)]
                # list to be dispatched
                task_list = [task for task in self.tasks \
                    if task.task_state is TASK_STATE.UNPROCESSED_UNASSIGNED]
                
                # delete event that is not confirmed
                ids = set([task.id for task in task_list])
                self.events = [eve for eve in self.events if eve.task.id not in ids]
                
                # replaning 
                unconfirmed_tasks = self.scheduler.method(task_list, self.tugs)
                unconfirmed_tasks = [i for i in unconfirmed_tasks \
                                    if i.task_state == TASK_STATE.UNPROCESSED_ASSIGNED]

                #regenerate task that is not confirmed before
                self.events = (
                    self.events + self.gen_event(unconfirmed_tasks, self.total_tasks, self.tasks, self.tugs, self.ships))
                
                # if the event type is canceled, remove all of the related events
                if event.type == EVENT_TYPE.CANCELED:
                    self.events = [eve for eve in self.events if eve.task.id != event.task.id]
                # if event.type == EVENT_TYPE.WORK_TIME_DELAY:
                #     for i in range(len(self.events)):
                #         #修正end work event發生的時間點
                #         if self.events[i].task.id == event.task.id and self.events[i].type == EVENT_TYPE.END_WORK:
                #             self.events[i].time = event.task.start_time + event.task.work_time
                #         #修正temp need後發生的work time delay
                        #       
            self.events.sort(key=lambda x: x.time)

    def gen_event(self, unconfirmed_tasks, total_tasks,tasks, tugs, ships):  # 把 queue合起
        queue = []
        queue = gen_confirm(unconfirmed_tasks, tugs, tasks, ships, 0.994) \
            + gen_workStartAndEnd(unconfirmed_tasks, total_tasks, tugs, tasks, ships) \
            + gen_tempNeed(unconfirmed_tasks, tugs, probability=0.3) \
            + gen_workTimeDelay(unconfirmed_tasks, tugs, probability=0.8)
        queue = sorted(queue, key=lambda x: x.time)
        return(queue)