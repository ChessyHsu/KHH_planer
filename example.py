from algo.estimator import Estimator
from algo.greedy.efficient import efficient_dispatch
from datetime import timedelta

from algo.model import TASK_STATE, TUG_STATE, SHIP_STATE, CHARGE_TYPE_LIST, CHARGE_TYPE
from algo.settings import PENALTY, WAITING_TIME, get_system_time
from algo.data_reading import get_pier_lanlng
from algo.utils.utility import find_required_tug, tug_to_charge_type, count_move_time, max_arrival_time, count_profit, showdetails
from algo.predict_worktime import predict_worktime
import copy 
from sys import stdout

def estimate_example():
    """
    An example to estimate the build-in efficient-greedy dispatching algorithm
    Take a look at efficient_dispatch() in algo/greedy/efficient.py
    """
    est = Estimator()
    est.set_print_all(True)
    est.run(efficient_dispatch,100,120)
    # est.run(greedy_dispatch)


def my_dispatch(tasks, tugs):
    """
    Implement your own dispatching algorithm
    All algorithms should read tasks and tugs, and modify their states after dispatching
    No return value 
    """
    # dispatch all tasks and modify the state of tasks and tugs

    tasks = copy.deepcopy(tasks)
    tugs = copy.deepcopy(tugs)
    # t=get_system_time()#now?
    #task
    todo = []
    for task in tasks:
        if task.task_state == TASK_STATE.UNPROCESSED_UNASSIGNED:
            todo.append(task)
    todo.sort(key=lambda x: x.start_time)
    #tug
    tugs_category={CHARGE_TYPE.TYPE_117:[], CHARGE_TYPE.TYPE_118:[], CHARGE_TYPE.TYPE_119:[], CHARGE_TYPE.TYPE_120:[], CHARGE_TYPE.TYPE_0:[]}
    for t in tugs:
        tugs_category[tug_to_charge_type([t])[0]].append(t)
    #assign
    for task in todo:
        stdout.write("Dispathching task {} ...\n".format(task.id))
        required_tugs_list = find_required_tug(task.ship.weight, task.tug_cnt)
        cand=[]
        if task.tug_cnt==1:
            for i in tugs_category[required_tugs_list[0]]:
                mi = i.next_available_time+count_move_time(task.ship_state, i.pos, task.start)
                early=task.start_time-mi
                cand.append([[i], early, early])
        else:
            for i in tugs_category[required_tugs_list[0]]:
                for j in tugs_category[required_tugs_list[1]]:
                    #arrival time
                    mi = task.start_time-i.next_available_time-count_move_time(task.ship_state, i.pos, task.start)
                    mj = task.start_time-j.next_available_time-count_move_time(task.ship_state, j.pos, task.start)
                    early=max(mi,mj)
                    wait=mi+mj
                    cand.append([[i,j], early, wait])
        cand.sort(key=lambda x: (x[1], x[2]))
        ontime=False
        for c in cand:
            if c[1]>=timedelta(minutes=0):
                ontime=True
                break
        best_set=[]
        if ontime:
            minpos=timedelta(minutes=100000)
            for c in cand:
                if c[1]>=timedelta(minutes=0) and c[1]<minpos:
                    minpos=c[1]
                    best_set=[i for i in c[0]]
        else:
            maxneg=timedelta(minutes=-100000)
            for c in cand:
                if c[1]>maxneg:
                    maxneg=c[1]
                    best_set=[i for i in c[0]]
        # Modify the task_state , work_time, assigned_tugs, start_time of the task 
        work_time = predict_worktime(task, best_set)
        task.task_state = TASK_STATE.UNPROCESSED_ASSIGNED
        task.work_time = work_time
        task.tugs = best_set
        arrival_time = max_arrival_time(task, best_set)
        temp = count_profit(task, best_set, work_time, arrival_time)
        task.delay_time = timedelta(minutes=temp["total_waiting_cost"] / PENALTY)
        task.start_time = max(arrival_time, task.start_time)

        for i in range(len(task.tugs)):
            # task.tugs[i].next_available_time = task.start_time + work_time
            task.tugs[i].pos = get_pier_lanlng(task.to)

        for tug in best_set:
            for i in range(len(tugs)):
                if tugs[i].tug_id == tug.tug_id:
                    tugs[i].next_available_time = task.start_time + work_time
                    tugs[i].pos = get_pier_lanlng(task.to)
    return tasks
def my_dispatch1(tasks, tugs):
    # dispatch all tasks and modify the state of tasks and tugs
    tasks = copy.deepcopy(tasks)
    tugs = copy.deepcopy(tugs)
    # t=get_system_time()#now?
    #task
    todo = []
    for task in tasks:
        if task.task_state == TASK_STATE.UNPROCESSED_UNASSIGNED:
            todo.append(task)
    todo.sort(key=lambda x: x.start_time)
    #tug
    tugs_category={CHARGE_TYPE.TYPE_117:[], CHARGE_TYPE.TYPE_118:[], CHARGE_TYPE.TYPE_119:[], CHARGE_TYPE.TYPE_120:[], CHARGE_TYPE.TYPE_0:[]}
    for t in tugs:
        tugs_category[tug_to_charge_type([t])[0]].append(t)
    #assign
    for task in todo:
        stdout.write("Dispathching task {} ...\n".format(task.id))
        required_tugs_list = find_required_tug(task.ship.weight, task.tug_cnt)
        cand=[]
        if task.tug_cnt==1:
            for i in tugs_category[required_tugs_list[0]]:
                m=count_move_time(task.ship_state, i.pos, task.start)
                mi = i.next_available_time+m
                early=task.start_time-mi
                cand.append([[i], m, early, early])
        else:
            for i in tugs_category[required_tugs_list[0]]:
                for j in tugs_category[required_tugs_list[1]]:
                    #arrival time
                    m=count_move_time(task.ship_state, i.pos, task.start)
                    mm=count_move_time(task.ship_state, j.pos, task.start)
                    mi = task.start_time-i.next_available_time-m
                    mj = task.start_time-j.next_available_time-mm
                    early=max(mi,mj)
                    wait=mi+mj
                    cand.append([[i,j], max(m, mm), early, wait])
        # cand.sort(key=lambda x: (-x[1], x[2]))
        ontime=True
        # for c in cand:
        #     if c[2]>=timedelta(minutes=0):
        #         ontime=True
        #         break
        best_set=[]
        if ontime:
            minpos=timedelta(minutes=100000)
            for c in cand:
                if c[1]<minpos:
                    minpos=c[1]
                    best_set=[i for i in c[0]]
        # else:
        #     maxneg=timedelta(minutes=-100000)
        #     for c in cand:
        #         if c[2]>maxneg:
        #             maxneg=c[2]
        #             best_set=[i for i in c[0]]
        # Modify the task_state , work_time, assigned_tugs, start_time of the task 
        work_time = predict_worktime(task, best_set)
        task.task_state = TASK_STATE.UNPROCESSED_ASSIGNED
        task.work_time = work_time
        task.tugs = best_set
        arrival_time = max_arrival_time(task, best_set)
        temp = count_profit(task, best_set, work_time, arrival_time)
        task.delay_time = timedelta(minutes=temp["total_waiting_cost"] / PENALTY)
        task.start_time = max(arrival_time, task.start_time)

        for i in range(len(task.tugs)):
            # task.tugs[i].next_available_time = task.start_time + work_time
            task.tugs[i].pos = get_pier_lanlng(task.to)

        for tug in best_set:
            for i in range(len(tugs)):
                if tugs[i].tug_id == tug.tug_id:
                    tugs[i].next_available_time = task.start_time + work_time
                    tugs[i].pos = get_pier_lanlng(task.to)
    return tasks
def my_dispatch2(tasks, tugs):
    return tasks
def estimate_my_algorithm():
    """
    The basic way to estimate your algorithm
    """
    est = Estimator()
    # determine the output format (default is False, which means only print the summary)
    est.set_print_all(False)
    # est.run(my_dispatch, 100, 120)
    est.run(my_dispatch1,100,120)
# estimate_example()
estimate_my_algorithm()
