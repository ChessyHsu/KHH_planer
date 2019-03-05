"""parameters of the system
"""
from enum import Enum
from datetime import datetime

class DISPATCH_METHOD(Enum):
    GREEDY = 1
    EFFICIENT = 2
    RANDOM = 3

# speed of tug
TUG_SPEED = 10

# speed of ship
SHIP_SPEED = 10

# duration of routine planning
ROUTINE_DURATION = 60

# distributing method
CURRENT_METHOD = DISPATCH_METHOD.EFFICIENT 

# penalty
PENALTY = 1

#oil price
OIL_PRICE = 0.07289

# system time
SYSTEM_TIME = datetime(2017, 1, 2, 0, 0, 0, 0)
