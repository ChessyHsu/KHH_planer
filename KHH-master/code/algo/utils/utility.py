from model import TASK_STATE, TUG_STATE, SHIP_STATE, CHARGE_TYPE_LIST, TUG, TASK, SHIP, CHARGE_TYPE
from predict_worktime import predict_worktime
from datetime import datetime, timedelta
from data_reading import get_pier_lanlng
import math
from itertools import combinations
from settings import PENALTY, OIL_PRICE, TUG_SPEED
from random import randint

def tug_to_charge_type(tug_set):
    return([tug.type for tug in tug_set])

def find_required_tug(weight, tug_cnt):
    """
    Args:
        weight (TASK.ship.weight) : ship weight
        tug_cnt (int):              the required number of tugs
    Returns:
        required_tug_list([CHARGE_TYPE]): a list of required tug type
    """
    tug_cnt -= 1
    if weight <= 5000:
        return([[CHARGE_TYPE.TYPE_117], [CHARGE_TYPE.TYPE_117, CHARGE_TYPE.TYPE_117]][tug_cnt])
    elif  weight <= 10000:
        return ([[CHARGE_TYPE.TYPE_118], [CHARGE_TYPE.TYPE_117, CHARGE_TYPE.TYPE_117]][tug_cnt])
    elif  weight <= 15000:
        return ([[CHARGE_TYPE.TYPE_118], [CHARGE_TYPE.TYPE_117, CHARGE_TYPE.TYPE_118]][tug_cnt])
    elif  weight <= 30000:
        return ([[CHARGE_TYPE.TYPE_118], [CHARGE_TYPE.TYPE_118, CHARGE_TYPE.TYPE_119]][tug_cnt])
    elif  weight <= 45000:
        return ([[CHARGE_TYPE.TYPE_120], [CHARGE_TYPE.TYPE_120, CHARGE_TYPE.TYPE_120]][tug_cnt])
    elif weight <= 60000:
        return ([[CHARGE_TYPE.TYPE_120], [CHARGE_TYPE.TYPE_120, CHARGE_TYPE.TYPE_120]][tug_cnt])
    elif weight <= 100000:
        return ([[CHARGE_TYPE.TYPE_0], [CHARGE_TYPE.TYPE_0, CHARGE_TYPE.TYPE_0]][tug_cnt])
    else:
        return ([CHARGE_TYPE.TYPE_0, CHARGE_TYPE.TYPE_0])


# 找到目前可用拖船的所有拖船組合
def find_possible_set(tugs, required_tugs_list):
    """
    Args:
        tugs ([TUG]): a list of available tugs
        required_tug_list ([CHARGE_TYPE]): a list of required_tug_list
    Returns:
        possible_set ([(TUG)]): list of tuples of tugs
    """
    n = len(required_tugs_list)

    return(list(combinations(tugs, n)))

# 一組拖船組合是否有符合required_tug_list的派遣規則（篩選possible_set）

# 所有拖船組合皆抵達的時間（最晚拖船抵達時間）
def max_arrival_time(task, tug_set):
    """
        Args:
            Task(TASK): a task
            tug_set([TUG]):a list of tug
        Returns:
            max_arrival_time(datetime):
    """

    arv_time = [count_move_time(task.ship_state, tug.pos, task.start) + tug.next_available_time \
            for tug in tug_set]
    return(max(arv_time))


def count_move_dis(state, start, to, velo=TUG_SPEED):
    """
        Args:
            state(TASK_STATE)
            start((float, float))
            to(int)
        Returns:
            move_time(timedelta)
    """
    to = harbor_to_pos(to) if state == SHIP_STATE.IN else get_pier_lanlng(to)
    dis = count_dis(float(start[0]), float(start[1]), float(to[0]), float(to[1]))
    return dis

def count_move_time(state, start, to, velo=TUG_SPEED):
    """
        Args:
            state(TASK_STATE)
            start((float, float))
            to(int)
        Returns:
            move_time(timedelta)
    """
    dis = count_move_dis(state, start, to, velo)
    return timedelta(minutes = ((dis / 1852) / (velo / 60)))

# 查詢harbor的經緯度
def harbor_to_pos(pier):
    ## State is IN
    harbor_pos = {9001: (22.616677, 120.265942),
                9002: (22.552638, 120.316716)}

    return(harbor_pos[pier])
# 用兩者的經緯度計算直線距離


def count_dis(base_lng, base_lat, lng, lat):
    """
        Args:
            base_lng(float)
            base_lat (float)
            lng(float)
            lat(float)
        Returns:
            dist(float)
    """
    lon1, lat1, lon2, lat2 = map(math.radians, [base_lng, base_lat, lng, lat])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat/2) ** 2 + math.cos(lat1) * \
        math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    r = 6371
    return c * r * 1000

# 計算價錢
def count_profit(Task, tug_set, work_time, arrival_time):
    """
        Args:
            Task(TASK)
            tug_set([TUG])
            work_time(timedelta)
            arrival_time(datetime)
        Returns:
            total_profit(int):the total profit of this pair

    """
    total_waiting_cost = 0
    total_moving_cost = 0
    total_revenue = 0
    total_profit = 0
    move_time = []
    charge = []
    required_tug_set = find_required_tug(Task.ship.weight, Task.tug_cnt)

    if not required_tug_set:
        charge = charge_type_to_price(tug_set, tug_set)
    else:
        charge = charge_type_to_price(tug_set, required_tug_set)

    for i in range(len(tug_set)):
        move_time.append(count_move_time(Task.ship_state, tug_set[i].pos, Task.start, velo = 10))
        move_dis = count_move_dis(Task.ship_state, tug_set[i].pos, Task.start, velo = 10)
        if move_time[i] + work_time < timedelta(minutes=60):
            total_revenue += charge[i]
            total_moving_cost += OIL_PRICE * move_dis
        else:
            time = 0
            time = math.ceil(((move_time[i] + work_time - timedelta(minutes = 60)).seconds /60) / 30) * 30 + 60
            total_revenue += (charge[i] * time/ 60)
            total_moving_cost += (OIL_PRICE * move_dis)
    delay_time = 0 if arrival_time <= Task.start_time else ((arrival_time - Task.start_time).seconds / 60)
    if arrival_time - Task.start_time > timedelta(seconds = 0):
        total_waiting_cost = PENALTY * delay_time
    total_profit = total_revenue - total_moving_cost - total_waiting_cost
    return ({"total_revenue":total_revenue,"total_waiting_cost":total_waiting_cost,"total_moving_cost":total_moving_cost,"total_profit":total_profit})

# 會找出各艘拖船較低的價錢


def charge_type_to_price(tug_list, required_tug_list):
    price = []
    tug_list = sorted(tug_list, key=(lambda tug: tug.type))
    required_tug_list.sort()
    price_dict = {117: 7395, 118: 10846, 119: 19720, 120: 22310, 130: 32000}
    for i in range(len(tug_list)):
        price.append(
            min(price_dict[required_tug_list[i]], price_dict[tug_list[i].type]))
    return (price)


def find_best_set(tug_set, task):
    max_profit = 0
    work_time = 0
    best_set = []
    for tugs in tug_set:
        wt = predict_worktime(task, tugs)
        arv_time = max_arrival_time(task, tugs)
        result = count_profit(task, tugs, wt, arv_time)
        if result['total_profit'] > max_profit:
            max_profit = result['profit']
            best_set = tugs
            work_time = wt

    return {"work_time": work_time, "best_set": best_set,"max_profit":max_profit}

def update_start_time(task):
    total_time = [tug.next_available_time + \
    count_move_time(task.ship_state, tug.pos, task.start) for tug in task.tugs]
    task.start_time = max(max(total_time), task.start_time)

def showdetails(task, method):
    task.sort(key=(lambda x: x.id))
    revenue = 0
    waiting_cost = 0
    moving_cost = 0
    profit = 0
    for i in task:
        i.show()
        print("* Required Tugs:", end=" ")
        print([i.value for i in find_required_tug(i.ship.weight, i.tug_cnt)])
        print("* Dispatched Tugs", end=" ")
        print([i.value for i in tug_to_charge_type(i.tugs)])
        print("")
        a = (count_profit(i, i.tugs, i.work_time, max_arrival_time(i, i.tugs)))
        print("* Revenue: {}\n* Waiting_cost: {} \n* Moving_cost: {}\n* Profit: {}\n".format(a['total_revenue'],a['total_waiting_cost'],a['total_moving_cost'],a['total_profit']))
        revenue += a['total_revenue']
        waiting_cost += a['total_waiting_cost']
        moving_cost += a['total_moving_cost']
        profit += a['total_profit']
    print("======== {}_SUMMARY ========".format(method))
    print("Revenue: {}\nTotal_waiting_cost: {}\nTotal_moving_cost: {}\nProfit: {}".format(revenue,waiting_cost,moving_cost,profit))
