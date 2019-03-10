"""All EVENT_TYPEs which calls dispatching algorithm again
"""

from enum import Enum, IntEnum
from .model import TASK_STATE, TUG_STATE, SHIP_STATE, ADD_TUG
import copy
from .utils.utility import get_pier_lanlng, max_arrival_time, count_move_time
from .predict_worktime import predict_worktime
from datetime import timedelta
from .settings import get_system_time


class EVENT_TYPE(Enum):
    """All kinds of EVENT_TYPEs which trigger planning algorithm

    Attributes:
        ROUTINE:            dispatch every one hour
        SHIP_DELAY:         delay caused by the ship
        TUG_DELAY:          delay caused by the tug
        UNIDENTIFIED_DELAY: delay occurs under unidentified situation
        MISMATCH:           the previous assignment is refused by the pilot
        CANCELED:           the task is canceled
    """
    # 每個task至少要發生其一的event
    CONFIRM_TASK = 'confirm_task'
    DENY_AND_CONFIRM = 'deny_and_confirm'

    CANCELED = 'canceled'

    START_TIME_DELAY = 'start_time_delay'
    WORK_TIME_DELAY = 'work_time_delay'

    # temp need & add tug
    TEMP_NEED = 'temp_need'

    START_WORK = 'start_work'
    END_WORK = 'end_work'


class Event():
    def __init__(self, type, task, tug_list, task_list, time):
        self.type = type
        self.task = task
        self.tug_list = tug_list
        self.task_list = task_list
        self.time = time

    def __str__(self):
        return ("[{}] Task {} happens at {}"
                .format(self.type.name, self.task.id, self.time.strftime("%Y-%m-%d %H:%M")))


class Confirm_task(Event):
    def __init__(self, task, tug_list, ship_list, task_list, time):
        Event.__init__(self, type=EVENT_TYPE.CONFIRM_TASK, task=task, tug_list=tug_list,
                    task_list=task_list, time=time)
        self.ship_list = ship_list

    def handle(self):
        # update the info of task
        for task in range(len(self.task_list)):
            if self.task.id == self.task_list[task].id:
                # replace the global_task with confirmed task
                self.task_list[task] = (self.task) 


        # update the info of tug
        for t in range(len(self.task.tugs)):
            for i in range(len(self.tug_list)):
                global_tug = self.task.tugs[t]
                if self.tug_list[i].tug_id == global_tug.tug_id:
                    last_time = self.task.start_time + self.task.work_time
                    if self.tug_list[i].next_available_time < last_time:
                        self.tug_list[i].next_available_time = last_time
                        self.tug_list[i].pos = get_pier_lanlng(self.task.to)
                    break

        # update the info of ship
        for i in range(len(self.ship_list)):
            if self.task.ship.ship_id == self.ship_list[i].ship_id:
                self.ship_list[i] = (self.task.ship)
        return


class Deny_and_confirm(Event):
    def __init__(self, task, required_tug, tug_list, task_list, time):
        Event.__init__(self, type=EVENT_TYPE.DENY_AND_CONFIRM, task=task, tug_list=tug_list,
                    task_list=task_list, time=time)
        self.required_tug = required_tug

    def handle(self):
        # replace the tugs with designated tugs
        self.task.tugs = self.required_tug

        # update the start time of the task
        self.task.start_time = max(
            self.task.start_time, max_arrival_time(self.task, self.required_tug))
        for i in range(len(self.required_tug)):
            self.required_tug[i].next_available_time = self.task.start_time + self.task.work_time

        # update global info of tugs
        for tug in self.required_tug:
            for global_tug in self.tug_list:
                if tug.tug_id == global_tug.tug_id:
                    global_tug.next_available_time = tug.next_available_time

        # confirm the task
        for t in range(len(self.task_list)):
            if self.task.id == self.task_list[t].id:
                # replace the global_task with confirmed task
                self.task_list[t] = (self.task)
            
        # update the info of tug
        for i in range(len(self.tug_list)):
            for t in range(len(self.tug_list)):
                global_tug = self.tug_list[t]
                if self.tug_list[i].tug_id == global_tug.tug_id:
                    last_time = self.task.start_time + self.task.work_time
                    if self.tug_list[i].next_available_time < last_time:
                        self.tug_list[i].next_available_time = last_time
                        self.tug_list[i].pos = get_pier_lanlng(self.task.to)
                    break
        return

class Start_work(Event):
    def __init__(self, task, task_list, tug_list, ships, time):
        Event.__init__(self, type=EVENT_TYPE.START_WORK, task=task, tug_list=tug_list,
                    task_list=task_list, time=time)
        self.ships = ships

    def handle(self):
        for i in range(len(self.task_list)):
            if self.task_list[i].id == self.task.id:
                self.task_list[i].task_state = TASK_STATE.PROCESSING_ASSIGNED


class End_work(Event):
    def __init__(self, task, tug_list, task_list, total_task_list, ships, time):
        Event.__init__(self, type=EVENT_TYPE.END_WORK, task=task, tug_list=tug_list,
                    task_list=task_list, time=time)
        self.ships = ships
        self.total_task_list = total_task_list

    def handle(self):
        self.task.state = TASK_STATE.PROCESSED
        for tug in self.tug_list:
            for global_tug in self.tug_list:
                if tug.tug_id == global_tug.tug_id:
                    global_tug.state = TUG_STATE.FREE
                    global_tug.pos = tug.pos

        for i in range(len(self.task_list)):
            if self.task_list[i].id == self.task.id:
                self.task_list[i].task_state = TASK_STATE.PROCESSED
        
        for i in range(len(self.total_task_list)):
            for j in range(len(self.task_list)):
                if self.total_task_list[i].id == self.task.id \
                    and self.task_list[j].id == self.task.id :
                    self.total_task_list[i] = self.task_list[j]

class WorkTimeDelay(Event): 

    def __init__(self, task, tug_list, delay_time, task_list, time):
        Event.__init__(self, type=EVENT_TYPE.WORK_TIME_DELAY, task=task, tug_list=tug_list,
                    task_list=task_list, time=time)
        self.delay_time = delay_time

    def handle(self):
        for i in range(len(self.task_list)):
            if self.task_list[i].id == self.task.id:
                self.task_list[i].work_time += self.delay_time
                break
        self.task.work_time += self.delay_time
        for i in range(len(self.tug_list)):
            self.tug_list[i].next_available_time += self.delay_time
        return


# Add tug or mismatch, after confirm
class Temp_need(Event):
    def __init__(self, task, extra_tug, tug_list, task_list, time):
        Event.__init__(self, type=EVENT_TYPE.TEMP_NEED, task=task, tug_list=tug_list,
                    task_list=task_list, time=time)
        self.extra_tug = extra_tug
        
    def handle(self):
        for i in range(len(self.task_list)):
            if self.task_list[i].id == self.task.id:
                for l in range(len(self.tug_list)):
                    if self.extra_tug[0].tug_id == self.tug_list[l].tug_id:
                        # edit the add_tug start_time 
                        start_time = max(self.tug_list[l].next_available_time,get_system_time()) + count_move_time(self.task.ship_state,self.tug_list[l].pos,self.task.start)
                        self.task_list[i].add_tug.append((ADD_TUG(self.extra_tug[0], start_time)))
                        # edit task work_time
                        if self.tug_list[l].next_available_time > get_system_time():
                            wait_extra_tug_finish_last_work_time = self.tug_list[l].next_available_time - get_system_time() 
                            remain_work_time = self.task_list[i].start_time + self.task_list[i].work_time - get_system_time()
                            self.tug_list[l].next_available_time += (remain_work_time + \
                                count_move_time(self.task.ship_state,self.tug_list[l].pos,self.task.start))
                            self.task_list[i].work_time += ( wait_extra_tug_finish_last_work_time \
                                 + count_move_time(self.task.ship_state,self.tug_list[l].pos,self.task.start))
                            
                        else:
                            remain_work_time = self.task_list[i].start_time + self.task_list[i].work_time - get_system_time()
                            self.tug_list[l].next_available_time += (remain_work_time + \
                                count_move_time(self.task.ship_state,self.tug_list[l].pos,self.task.start))
                            self.task_list[i].work_time += count_move_time(self.task.ship_state,self.tug_list[l].pos,self.task.start)
        
            
class Canceled(Event):
    def __init__(self, task, task_list, time):
        Event.__init__(self, type=EVENT_TYPE.CANCELED, task=task, tug_list=None,
                    task_list=task_list, time=time)

    def handle(self):
        if self.task.start_time < self.time:
            for i in range(len(self.task.tugs)):
                self.task.tugs[i].state = TUG_STATE.FREE
                self.task.tugs[i].next_available_time = self.time
            self.task.work_time = self.time - self.task.start_time
            self.task.state = TASK_STATE.CANCELED

        # if the revenue of the profit is 0, then cancel it directly
        else:  
            for i in range(len(self.task_list)):
                if self.task_list[i].id == self.task_list[i].id:
                    self.task_list[i].state = TASK_STATE.CANCELED
                    # self.task_list.remove(task)

# class AddTug(Event):  # Mismatch 的 processing 版
#     def __init__(self, task, extra_tug, task_list, tug_list, time):
#         Event.__init__(self, type = EVENT_TYPE.ADD_TUG, task = task, tug_list = tug_list,\
#                         task_list = task_list, time = time)
#         self.extra_tug = extra_tug

#     def handle(self):
#         for task in self.task_list:
#             if task.id == self.task.id: #add tug 的 task
#                 task.tugs = self.task # assign tugs
#                 task.task_state = TASK_STATE.UNPROCESSED_ASSIGNED # state -> assigned
#                 # modify start time

#                 # update the start time of the task
#                 task.start_time = max(task.start_time,max_arrival_time(task, self.required_tug))
#                 for i in self.required_tug:
#                     i.next_available_time = task.start_time + task.work_time

#                 task.work_time = predict_worktime(task, self.required_tug)
#     def __str__(self):
#         return ("[EVENT_TYPE] Task {} needs more tug_list: {}"
#             .format(self.task.id, [tug.id for tug in self.required_tug]))
