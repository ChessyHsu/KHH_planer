"""parameters of the system
"""
from enum import Enum
from datetime import datetime, timedelta


class DISPATCH_METHOD(Enum):
    GREEDY = 1
    EFFICIENT = 2
    RANDOM = 3


TUG_SPEED = 8

SHIP_SPEED = 10

# duration of routine planning
ROUTINE_DURATION = 60

CURRENT_METHOD = DISPATCH_METHOD.EFFICIENT

PENALTY = 1

OIL_PRICE = 0.07289

SYSTEM_TIME = datetime(2017, 1, 2, 6, 14, 0, 0)

WAITING_TIME = timedelta(minutes=17)


def set_system_time(time):
    global SYSTEM_TIME
    SYSTEM_TIME = time
    return (SYSTEM_TIME)


def set_method(method):
    global CURRENT_METHOD
    if "e" in method:
        CURRENT_METHOD = DISPATCH_METHOD.EFFICIENT
    elif "g" in method:
        CURRENT_METHOD = DISPATCH_METHOD.GREEDY
    else:
        CURRENT_METHOD = DISPATCH_METHOD.RANDOM
    return (CURRENT_METHOD)


def get_system_time():
    global SYSTEM_TIME
    return (SYSTEM_TIME)
