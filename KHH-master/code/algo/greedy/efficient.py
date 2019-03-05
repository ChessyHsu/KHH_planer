"""greedy dispatch v2
"""
from model import TASK_STATE, TUG_STATE, SHIP_STATE, CHARGE_TYPE_LIST, TUG, TASK, SHIP
from settings import SYSTEM_TIME, PENALTY, OIL_PRICE
from datetime import datetime, timedelta
from data_reading import get_pier_lanlng
from utils.utility import harbor_to_pos, update_start_time , find_required_tug, tug_to_charge_type, count_move_time, max_arrival_time, count_profit, showdetails
from predict_worktime import predict_worktime
from his.data import history_tasks, history_tugs

from sys import stderr
import time
import copy
import math
import itertools

def efficient_dispatch(tasks, tugs):
    """
    Args:
        tasks ([Task]): a list which stores the tasks to be planned

    Returns:
        tasks ([Task]): a list which stores the current processing and unprocessed tasks
    """
    #tugs = [tug for tug in tugs if tug.state is not TUG_STATE.UNAVAILABLE]
    stderr.write(
        "Dispatching {} tasks with Simple Greedy...\n".format(len(tasks)))
    tasks.sort(key=lambda x: x.start_time)
    for task in tasks:
        tug_set = []
        stderr.write("Dispathching task {} ...\n".format(task.id))
        # 先用required_tug_set算出這個task的work_time
        required_tugs_list = find_required_tug(task.ship.weight, task.tug_cnt)

        tug_set = sorted(tugs, key=lambda x: x.type)
        best_set = []
        for i in required_tugs_list:
            for l in range(len(tug_set)):
                temp = count_move_time(
                    task.ship_state, tug_set[l].pos, task.start, velo=10)
                if tug_to_charge_type(tug_set)[l] >= i and tug_set[l].next_available_time + temp - task.start_time < timedelta(minutes=0):
                    best_set.append(tug_set[l])
                    tug_set.remove(tug_set[l])
                    break

        work_time = predict_worktime(task, best_set)
        if not best_set:
            stderr.write("No best set!\n")
            continue

        # 更改每個tasks（複製的tasks）的
        # 1.task_state,
        # 2.work_time,
        # 3.tug(配對的tugs)
        # 4.調整tasks的開始時間
        task.task_state = TASK_STATE.UNPROCESSED_ASSIGNED
        task.work_time = work_time
        task.tugs = best_set
        update_start_time(task)

        for tug in task.tugs:
            tug.next_available_time = task.start_time + work_time
            tug.pos = harbor_to_pos(
                task.to) if task.ship_state == SHIP_STATE.OUT else get_pier_lanlng(task.to)

    return(tasks)

