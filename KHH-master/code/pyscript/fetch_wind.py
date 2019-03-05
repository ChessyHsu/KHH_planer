#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 21 10:40:43 2018

@author: shinying.lee
"""
import pandas as pd
from datetime import datetime

weather = pd.read_excel('data/weather_full.xlsx')

stop = datetime(2018, 1, 1, 0, 0, 0)
wind = pd.Series([0.0]*365*24)
date = pd.Series([0]*365*24)
i = 0
j = 0
t = weather.偵測時間[i]
while t < stop:
    tomorrow = (weather.偵測時間[i].hour + 1) % 24
    sum_wind = 0
    count = 0
    while weather.偵測時間[i].hour != tomorrow:
        sum_wind += weather.一港風力[i]
        i += 1
        count += 1
    wind[j] = float(sum_wind) / count
    date[j] = datetime(
                weather.偵測時間[i-1].year,
                weather.偵測時間[i-1].month,
                weather.偵測時間[i-1].day,
                weather.偵測時間[i-1].hour,
            )
    j += 1
    t = weather.偵測時間[i]

avg_wind = pd.DataFrame({
            'date' : date,
            'wind' : wind,
        })
    
avg_wind.to_excel("data/avg_wind.xlsx", index=False)