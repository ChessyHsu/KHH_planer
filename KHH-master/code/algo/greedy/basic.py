"""greedy dispatch v1
"""
from model import TASK_STATE, TUG_STATE, SHIP_STATE, CHARGE_TYPE_LIST, TUG, TASK, SHIP
from settings import SYSTEM_TIME, PENALTY, OIL_PRICE
from datetime import datetime, timedelta
from data_reading import get_pier_lanlng
from utils.utility import find_required_tug, find_possible_set, find_best_set, tug_to_charge_type, update_start_time, harbor_to_pos, get_pier_lanlng
from his.data import history_tasks, history_tugs
from sys import stderr

import math
import itertools
import copy


def greedy_dispatch(tasks, tugs):
    """
    Args:
        tasks ([Task]): a list which stores the tasks to be planned

    Returns:
        tasks ([Task]): a list which stores the current processing and unprocessed tasks
    """
    # 利用噸位尋找收費型號
    tugs = [tug for tug in tugs if tug.state is not TUG_STATE.UNAVAILABLE]
    #tugs = copy.deepcopy(tugs)
    stderr.write("Dispatching {} tasks with Simple Greedy...\n".format(len(tasks)))

    for task in tasks:
        stderr.write("Dispathching task {} ...\n".format(task.id))
        
        # required_tug_list (type):[收費型號] ex: [117,118]
        required_tugs_list = find_required_tug(task.ship.weight, task.tug_cnt)
        
        # possible set 是所有可用到的拖船組合
        # type: [TUG]
        # function: find_possible_set : 把已經預排的與正在工作的拖船剔除在拖船組合之外
        # 考慮_next_available_time
        possible_set = find_possible_set(tugs, required_tugs_list)
        alternative_set = []

        for s in possible_set:
            candidate = CHARGE_TYPE_LIST(tug_to_charge_type(s))
            required = CHARGE_TYPE_LIST(required_tugs_list)
            if candidate < required:
                alternative_set.append(s)

        possible_set = list(set(possible_set) - set(alternative_set))

        result = find_best_set(possible_set, task) if possible_set \
            else find_best_set(alternative_set, task)

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

