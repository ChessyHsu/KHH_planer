## Process history data
import pandas as pd
from sys import stderr
from model import SHIP, TASK, SIDE, SHIP_STATE, TUG, CHARGE_TYPE
from utils.utility import find_required_tug, find_possible_set, find_best_set, tug_to_charge_type, update_start_time, harbor_to_pos, get_pier_lanlng, max_arrival_time, showdetails
from datetime import datetime, timedelta
from settings import SYSTEM_TIME

def tug_no_to_hp(tug_no):
    dict = { 143 : 1800,
            145 : 1800,
            151 : 2400,
            152 : 2400,
            153 : 2400,
            155 : 2400,
            112 : 2400,
            241 : 2400,
            245 : 2400,
            321 : 3200,
            322 : 3200,
            101 : 3200,
            302 : 3200,
            104 : 3200,
            106 : 3200,
            108 : 3200,
            109 : 3200,
            303 : 3300,
            306 : 3400,
            308 : 3500,
            301 : 3600,
            161 : 4000,
            162 : 4000,
            163 : 4200,
            165 : 4200,
            401 : 4400,
            451 : 4500,
            171 : 5200,
            172 : 5200,
            181 : 6400,
            182 : 6400
        }
    return (dict[tug_no])


def hp_to_charge_type(hp):
    if hp <= 1800:
        return (CHARGE_TYPE.TYPE_117)
    elif hp <= 2400:
        return (CHARGE_TYPE.TYPE_118)
    elif hp <= 3200:
        return (CHARGE_TYPE.TYPE_119)
    elif hp <= 4000:
        return (CHARGE_TYPE.TYPE_120)
    else:
        return (CHARGE_TYPE.TYPE_0)

def tug_no_to_tug(tid):
    hp = (tug_no_to_hp(tid))
    tug = TUG(tid, (22.552638, 120.316716), hp_to_charge_type(hp), hp)
    return (tug)

def find_side(v):
    return([member for name, member in SIDE.__members__.items() if member.value == v][0])

def find_state(v):
    return([member for name, member in SHIP_STATE.__members__.items() if member.value == v][0])

def tug_last_info(main, row):
    last_pier = 0
    tug_no = main.iloc[row, :].tug
    for i in range(row-1, 0, -1):
        sh = main.iloc[i, :]
        if sh.tug == tug_no:
            if sh.sailing_status == 'I':
                last_pier = sh.place2

            elif sh.sailing_status == 'O':
                last_pier = int(sh.port)+9000

            elif sh.sailing_status == 'T':
                last_pier = sh.place2
            last_time = sh.max_end_time
            return([get_pier_lanlng(last_pier), last_time])
    return([get_pier_lanlng(1001), SYSTEM_TIME]) #no last place in history data



stderr.write("Reading History Data...\n")
cnt = 0
last_time = 0
tid_list = []
history_tugs = []
history_tasks = []
main = pd.DataFrame(pd.read_excel("../pyscript/data/main1010.xlsx"))

for row in (range(100, 120)):
    sh = main.iloc[row, :]
    if last_time != sh.start_time: 
        # create new ship and new task
        last_time = sh.start_time
        if sh.sailing_status == 'I':
            ship = (SHIP(ship_id = int(sh.ship_no), cur_pos = (
                0, 0), weight = sh.total_weight))  # temp place
            task = (TASK(i = cnt, ship = ship, ship_state = SHIP_STATE.IN, start_time = sh.pilot_ready_time,
                    start = int(sh.port) + 9000, dest = int(sh.place2), side = find_side(sh.park), tug_cnt = 1))
            task.work_time = timedelta(minutes = int(sh.min_work_time))
            history_tasks.append(task)
        elif sh.sailing_status == 'O':
            ship = (SHIP(ship_id = int(sh.ship_no), cur_pos = get_pier_lanlng(
                sh.place2), weight = sh.total_weight))
            task = (TASK(i = cnt, ship = ship, ship_state = SHIP_STATE.OUT, start_time = sh.pilot_ready_time,
                    dest = int(sh.port) + 9000, start = int(sh.place2), side = find_side(sh.park), tug_cnt = 1))
            task.work_time = timedelta(minutes = int(sh.min_work_time))
            history_tasks.append(task)

        elif sh.sailing_status == 'T':
            ship = (SHIP(ship_id = int(sh.ship_no), cur_pos = get_pier_lanlng(
                sh.place1), weight = sh.total_weight))
            task = (TASK(i = cnt, ship = ship, ship_state = SHIP_STATE.TRANSFER, start_time = sh.pilot_ready_time,
                    start = int(sh.place1), dest = int(sh.place2), side = find_side(sh.park), tug_cnt = 1))
            task.work_time = timedelta(minutes = int(sh.min_work_time))
            history_tasks.append(task)
        history_tasks[cnt].tugs = []
        history_tasks[cnt].tugs.append(tug_no_to_tug(sh.tug))
        cnt += 1
    else:
        history_tasks[cnt-1].tugs.append(tug_no_to_tug(sh.tug))
        history_tasks[len(history_tasks)-1].tug_cnt += 1

    if sh.tug in tid_list:
        continue

    tid_list.append(sh.tug)
    hp = (tug_no_to_hp(sh.tug))
    info = tug_last_info(main, row)
    history_tugs.append(TUG(sh.tug, info[0], hp_to_charge_type(hp), hp , next_available_time = info[1]))

## remove the task with tug_cnt > 2
## as we cannot find the required tug

for i in history_tasks:
    if i.tug_cnt >= 2:
        history_tasks.remove(i)
        continue



