"""greedy dispatch v1
"""
from model import TASK_STATE, TUG_STATE, SHIP_STATE, CHARGE_TYPE_LIST, TUG, TASK, SHIP
from settings import SYSTEM_TIME, PENALTY, OIL_PRICE
from datetime import datetime, timedelta
from data_reading import get_pier_lanlng
import math
import itertools
from utils.utility import find_best_set_without_oil, count_profit_without_oil, find_required_tug, find_possible_set, find_best_set, tug_to_charge_type, update_start_time, harbor_to_pos, get_pier_lanlng , max_arrival_time, showdetails 
import copy
from history_get_tug import tasklist as history_tasks
from history_get_tug import assigned_tugs, history_tugs
from test import tasks, ship, tugs0102
from sys import stderr
import time

def greedy_dispatch_without_oil_prof(tasks, tugs):
    """
    Args:
        tasks ([Task]): a list which stores the tasks to be planned

    Returns:
        tasks ([Task]): a list which stores the current processing and unprocessed tasks
    """

    # 3.order all the task by start_time
    # tasks = sorted(tasks,key = task.start_time)
    # 利用噸位尋找收費型號
    tugs = [tug for tug in tugs if tug.state is not TUG_STATE.UNAVAILABLE]
    
    stderr.write("Dispatching {} tasks with Simple Greedy...\n".format(len(tasks)))
    tasks.sort(key = lambda x: x.start_time)

    for task in tasks:
        
        stderr.write("Dispathching task {} ...\n".format(task.id))
        # 2. 挑出free的tug or next avliable time 在一小時之前的task
        # required_tug_list (type):[收費型號] ex: [117,118]
        required_tugs_list = find_required_tug(task.ship.weight, task.tug_cnt)
        # possible set 是所有可用到的拖船組合
        # type: [TUG]
        # function: find_possible_set : 把已經預排的與正在工作的拖船剔除在拖船組合之外
        # 考慮_next_available_time
        possible_set = find_possible_set(tugs, required_tugs_list)
        alternative_set = []

        required = CHARGE_TYPE_LIST(required_tugs_list)
        for s in possible_set:
            candidate = CHARGE_TYPE_LIST(tug_to_charge_type(s))
            if candidate < required:
                alternative_set.append(s)

        possible_set = list(set(possible_set) - set(alternative_set))
    
        if possible_set:
            possible_set.sort(key = lambda x : sum([abs(y[0]-y[1]) for y in zip(tug_to_charge_type(x), required.types)]), reverse = True)
        else:
            alternative_set.sort(key = lambda x : sum([abs(y[0]-y[1]) for y in zip(tug_to_charge_type(x), required.types)]), reverse = True)
        
        result = find_best_set_without_oil(possible_set, task) if possible_set \
            else find_best_set_without_oil(alternative_set, task)

        best_set = result['best_set']
        max_profit = result['max_profit']

        if not best_set:
            stderr.write("No best set!\n")
            continue

        # 更改每個tasks（複製的tasks）的
        # 1.task_state,
        # 2.work_time,
        # 3.tug(配對的tugs)
        # 4.調整tasks的開始時間
        task.task_state = TASK_STATE.UNPROCESSED_ASSIGNED
        task.work_time = result['work_time']
        task.tugs = best_set
        update_start_time(task)

        for tug in task.tugs:
            tug.next_available_time = task.start_time + result['work_time']
            tug.pos = harbor_to_pos(
                task.to) if task.ship_state == SHIP_STATE.OUT else get_pier_lanlng(task.to)

    return(tasks)

result = []
# result = greedy_dispatch_without_oil_prof(history_tasks, history_tugs)
# # print("Finish with penalty ${} and oil price ${}".format(PENALTY, OIL_PRICE)
start_time = time.time()
result = greedy_dispatch_without_oil_prof(history_tasks, history_tugs)
end_time  = time.time()
print("time",end_time-start_time)
showdetails(result, "Simple Greedy history")