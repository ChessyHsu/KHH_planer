import numpy as np
import pandas as pd
import sklearn
import pickle
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
import model
import datetime
import WorkingTimePrediction

class WorkTimePredictor(WorkTimePrediction):
    def classify_weight_level(w):
        level = {5000: 1, 10000: 2, 15000: 3,
                30000: 4, 45000: 5, 60000: 6, 100000: 7}
        for k in level:
            if w < k:
                return (level[k])
        return (8)

    def dfCreator(Task, tug_set):
        # port
        port = 0
        if Task._from == 9001:
            port = 1
        else:
            port = 2
        # reverse
        reverse = 0
        if Task._ship_state == 'I':
            if Task._from == 9001:
                if Task._side == 'L':
                    reverse = bool(df_reverse1.loc[9001, int(Task._to)])
                else:
                    reverse = not(bool(df_reverse1.loc[9001, int(Task._to)]))
            elif Task._from == 9002:
                if Task._side == 'L':
                    reverse = bool(df_reverse1.loc[9002, int(Task._to)])
                else:
                    reverse = not(bool(df_reverse1.loc[9002, int(Task._to)]))
        elif Task.ship_state == 'T':
            reverse = bool(df_reverse2.loc[int(Task._from), int(Task._to)])
        # weekday
        weekday = Task._start_time.weekday() + 1
        # hour
        hour = Task._start_time.hour
        # avg_hp
        avg_hp = 0
        for i in len(tug_set):
            sum = i._hp
        avg_hp = sum / len(tug_set)
        df = pd.DataFrame([[Task._ship_state, port, len(tug_set), Task._ship._weight, classify_weight_level(Task._ship._weight), dist_pier.loc[int(
            Task._from), int(Task._to)], Task._wind, Task._side, reverse, date.month(Task._start_time), weekday, hour, avg_hp]])
        return (df)
    def predict(Task, tug_set):
        df = dfCreator(Task, tug_set)
        pred_time = WorkTimePrediction(df).run()
        return (pred_time)