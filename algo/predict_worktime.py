"""providing worktime prediction
"""

import numpy as np
import pandas as pd
import datetime
from datetime import timedelta
from .outsourcing.WorkTimePrediction import WorkTimePrediction
from .data_reading import get_pierToPier_dist, get_portToPier_dist, get_reverse
from .utils.utility import classify_weight_level


def predict_worktime(task, tug_set):
    df = dfCreator(task, tug_set)
    return (timedelta(minutes=WorkTimePrediction().run(df)[0]))


def dfCreator(task, tug_set):
    port = 1 if task.start == 9001 else 2
    tug_cnt = len(tug_set)
    weight_lev = classify_weight_level(task.ship.weight)

    # dist = 1502.6
    dist = get_pierToPier_dist(task.start, task.to)

    # wind
    wind = 3

    # find reverse
    reverse = get_reverse(task)

    # time
    time = task.start_time
    month = time.month
    weekday = time.weekday() + 1
    hour = time.hour

    # avg_hp
    avg_hp = 0
    mysum = 0
    for i in range(len(tug_set)):
        mysum = mysum + tug_set[i].hp
    avg_hp = mysum / len(tug_set)

    # create dataframe
    df = pd.DataFrame([[task.ship_state,
                        port,
                        tug_cnt,
                        task.ship.weight,
                        weight_lev,
                        dist,
                        wind,
                        task.side,
                        reverse,
                        month,
                        weekday,
                        hour,
                        avg_hp]],
                      columns=list(["sailing_status",
                                    "port",
                                    "tug_cnt",
                                    "total_weight",
                                    "weight_level",
                                    "dist",
                                    "wind",
                                    "park",
                                    "reverse",
                                    "month",
                                    "weekday",
                                    "hour",
                                    "avg_hp"]))
    return (df)
