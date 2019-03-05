"""The main interface of distributing algorithm
"""

from scheduler import Scheduler
from settings import ROUTINE_DURATION, CURRENT_METHOD
from his.data import  history_tugs, history_tasks
from utils.utility import showdetails
from settings import SYSTEM_TIME
from greedy.basic import greedy_dispatch

from datetime import datetime
def main():
    scheduler = Scheduler(CURRENT_METHOD)
    tasks = history_tasks
    tugs = history_tugs
    # check new coming event
    # for task in tasks:
    #     if task.start_time <= SYSTEM_TIME + ROUTINE_DURATION:
    #         tasks.append(task)
    #     else: 
    #         break
    showdetails(scheduler.exec(tasks, tugs), CURRENT_METHOD.name)




if __name__ == "__main__":
    main()