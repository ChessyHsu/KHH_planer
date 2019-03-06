""" define the model ex. Ship, Tug, Task ... etc
"""
from enum import Enum, IntEnum
from datetime import time, datetime, timedelta
from algo.settings import SHIP_SPEED, TUG_SPEED, SYSTEM_TIME


class Event(Enum):
    """All kinds of events which trigger planning algorithm

    Attributes:
        ROUTINE:            dispatch every one hour
        SHIP_DELAY:         delay caused by the ship
        TUG_DELAY:          delay caused by the tug
        UNIDENTIFIED_DELAY: delay occurs under unidentified situation
        MISMATCH:           the previous assignment is refused by the pilot
        BEFOREHAND:         any of the tugs finish task in advance
        CANCELED:           the task is canceled
    """

    ROUTINE = 'routine'
    CANCELED = 'canceled'

    TUG_DELAY = 'tug_delay'
    SHIP_DELAY = 'ship_delay'
    UNIDENTIFIED_DELAY = 'unidentified_delay'
    PIER_DELAY = 'pier_delay'

    MISMATCH = 'mismatch'
    BEFOREHAND = 'beforehand'

    ADD_TUG = 'add_tug'


class TUG_STATE(Enum):
    """States of tugs which are considered when planning

    Attributes:
        FREE:        a tug which is ready to work immediately
        BUSY:        a tug which is busy working on a specific tesk
        UNAVAILABLE: a tug which is either broken or out of order
    """
    FREE = 0
    BUSY = 1
    UNAVAILABLE = 2


class CHARGE_TYPE(IntEnum):
    """Types of tugs which are used in charging and planning.
    Values of attributes correpond to weights according to the dispatching rule
    """

    TYPE_117 = 117
    TYPE_118 = 118
    TYPE_119 = 119
    TYPE_120 = 120
    TYPE_0 = 130


class TASK_STATE(IntEnum):
    """States of task describing
        if tugs are assigned (UNASSIGNED or ASSIGNED)
        if the task is finished (UNPROCESSED, PROCESSING, or PROCESSED)
    """

    UNPROCESSED_UNASSIGNED = 0
    UNPROCESSED_ASSIGNED = 1
    PROCESSING_ASSIGNED = 2
    PROCESSED = 3
    CANCELED = 4


class SIDE(Enum):
    LEFT = 'L'
    RIGHT = 'R'
    OPTIONAL = 'O'


class SHIP_STATE(Enum):
    IN = 'I'
    OUT = 'O'
    TRANSFER = 'T'


class TUG():
    """Main entities to be planned

    Attributes:
        id (int):             ID of the tug
        pos ((float, float)): current position of the tug, a pair of latitude and lontitude
        type (CHARGE_TYPE):   charging type
        hp (int):             horsepower of the tug
        velo (int):           velocity, default 10kt
        state (TUG_STATE):    current state of the tug
        next_available_time:  if tug state is busy,we will recorded the time which it will finish the task
    """

    def __init__(self, tug_id, cur_pos, charge_type,
                hp, state=TUG_STATE.FREE, velo=TUG_SPEED, next_available_time=SYSTEM_TIME):
        self.tug_id = tug_id
        self.pos = cur_pos
        self.type = charge_type
        self.hp = hp
        self.state = state
        self.velo = velo
        self.next_available_time = next_available_time

    def __str__(self):
        return("TUG {}: type = {} hp = {} state = {} pos = {} next available time = {}".format(self.tug_id, self.type, self.hp, self.state, self.pos, self.next_available_time))


class ADD_TUG():
    def __init__(self, tug, start_moving_time):
        self.tug = tug
        self.start_moving_time = start_moving_time
    def __str__(self):
        return ("ADD_TUG {}: type = {} hp = {} state = {} pos = {} next available time = {}".format(self.tug.tug_id, self.tug.type, self.tug.hp, self.tug.state, self.tug.pos, self.tug.next_available_time))
        
# TUG list and TUG list 之間的比較
class CHARGE_TYPE_LIST(object):
    def __init__(self, charge_type_list):
        self.types = sorted(charge_type_list)

    def __eq__(self, other):
        other = other.types
        if len(self.types) != len(other):
            return (False)
        else:
            for i in range(len(self.types)):
                if self.types[i] != other[i]:
                    return (False)
        return (True)

    def __gt__(self, other):
        other = other.types
        if len(self.types) != len(other):
            return (False)
        else:
            for i in range(len(self.types)):
                if self.types[i] < other[i]:
                    return (False)
        return (True)

    def __ge__(self, other):
        return ((self > other) or (self == other))


class SHIP():
    """Characteristics of ships would be considered in planning

    Attributes:
        id (int):        ID of the ship
        pos ((int,int)): current position of the ship, a pair of latitude and longitude
        weight (int):    ship weight
        velo (int):      velocity, default 10kt
    """

    def __init__(self, ship_id, cur_pos, weight, velo=SHIP_SPEED):
        self.ship_id = ship_id
        self.pos = cur_pos
        self.weight = weight
        self.velo = velo

    def __str__(self):
        return ("SHIP {}: weight = {}".format(self.ship_id, self.weight))
        

class TASK():
    """
    Attributes:
    id (int):                  ID
    ship (SHIP):               ship
    tug_cnt (int):             the required number of tugs
    task_state (TASK_STATE):   task state
    ship_state (SHIP_STATE):   ship state
    start_time (datetime):     starting time
    delay_time (timedelta):    start time delay
    work_time (datetime) :     working time predicted by regression model
    start (int):               starting place, port number
    to (int):                  final place, port number
    side (SIDE):               a ship parks with its left or right side
    tugs ([TUG]):              a list of tug assigned to serve the ship
    add_tug ([TUG]):           a list of add tugs 
    """

    def __init__(self, i, ship, tug_cnt, ship_state, start_time, start, dest, side=SIDE.OPTIONAL, delay_time=timedelta(minutes=0)):
        self.work_time = timedelta(minutes=0)
        self.tugs = []
        self.add_tug = []
        self.task_state = TASK_STATE.UNPROCESSED_UNASSIGNED
        self.id = i
        self.ship = ship
        self.tug_cnt = tug_cnt
        self.ship_state = ship_state
        self.start_time = start_time
        self.start = start
        self.to = dest
        self.side = side
        self.delay_time = delay_time


    def __str__(self):
        return("TASK {}: ship {}\n* Depart at: {}\n* From {} to {}\n* Goes: {}\n* Side: {}\n* Delay_time: {}\n\n".format(
            self.id, self.ship.ship_id, self.start_time.strftime("%Y-%m-%d %H:%M"),
            self.start, self.to, self.ship_state.name, self.side.name, self.delay_time))

    def show(self):
        res = "======== Task {} Result ========\n".format(self.id)
        res += ("* Ship ID: {}\n" + 
                "* Ship State: {}\n" +
                "* Should Started at: {}\n" +
                "* Started at: {}\n" +
                "* Working time: {}\n" + 
                "* State: {}\n" +
                "* Weight: {}\n" +
                "* Delay_time: {}\n\n").format(
                    self.ship.ship_id,
                    self.ship_state.name,
                    (self.start_time-self.delay_time).strftime("%Y-%m-%d %H:%M"),
                    self.start_time.strftime("%Y-%m-%d %H:%M"), 
                    self.work_time, 
                    self.task_state.name, 
                    self.ship.weight, 
                    self.delay_time,
                )

        res += "* Tug Set: "
        for t in self.tugs:
            res += "{} ".format(t.tug_id)
        res += "\n"
        res += "* Add Tugs: "
        for t in self.add_tug:
            res += "{} ".format(t.tug.tug_id)
        print(res)
