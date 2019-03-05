"""greedy dispatch 
"""

import copy
from sys import stderr
from datetime import timedelta

from algo.model import TASK_STATE, TUG_STATE, SHIP_STATE, CHARGE_TYPE_LIST
from algo.settings import PENALTY, WAITING_TIME, get_system_time
from algo.data_reading import get_pier_lanlng
from algo.utils.utility import find_required_tug, tug_to_charge_type, count_move_time, max_arrival_time, count_profit, showdetails
from algo.predict_worktime import predict_worktime


def efficient_dispatch(tasks, tugs):
    """
    Args:
        tasks ([Task]): a list which stores the tasks to be planned
    Returns:
        tasks ([Task]): a list which stores the current processing and unprocessed tasks
    """
    tasks = copy.deepcopy(tasks)
    tugs = copy.deepcopy(tugs)
    tmp = []
    for task in tasks:
        if task.task_state == TASK_STATE.UNPROCESSED_UNASSIGNED:
            tmp.append(task)
            
    tasks = tmp
    tasks.sort(key=lambda x: x.start_time)
    stderr.write(
        "Dispatching {} tasks with Efficient Greedy...\n".format(len(tasks)))
            
    for task in tasks:
        stderr.write("Dispathching task {} ...\n".format(task.id))
        # Compute the require time with the required tugs
        required_tugs_list = find_required_tug(task.ship.weight, task.tug_cnt)
        tug_set = []
        # tug_set = sorted(tugs,key=lambda x: x.type)
        tug_set = sorted(tugs,key=lambda x: x.next_available_time)
        best_set = []
        for i in required_tugs_list:
            for l in list(tug_set):
                temp_move_time = count_move_time(task.ship_state, l.pos, task.start)
                if tug_to_charge_type([l])[0] >= i and \
                ((l.next_available_time + temp_move_time - task.start_time <= WAITING_TIME ) or \
                (l.next_available_time + temp_move_time - get_system_time() <= WAITING_TIME + (get_system_time() - task.start_time))):
                    best_set.append(copy.deepcopy(l))
                    tug_set.remove(l)
                    break

        if len(best_set) != len(required_tugs_list):
            stderr.write("No best set!\n")
            continue

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

    for i in range(len(tasks)):
        if tasks[i].tugs is None:
            tasks.remove(tasks[i])
    return(tasks)