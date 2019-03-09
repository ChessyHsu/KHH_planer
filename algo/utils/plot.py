import numpy as np
import random
import plotly.tools as pt
import plotly.plotly as pp
import plotly.figure_factory as ff
from datetime import datetime, timedelta
# from algo.his.data import history_tasks
from algo.utils.utility import count_move_time
pt.set_credentials_file(username='hanjuTsai', api_key='XEOnjaC9Om7WcOwgbRqs')
# pt.set_credentials_file(username='angyeahyeah6', api_key='heDVJdzx2KYVJAfpReWi')

number_of_colors = 100
color = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(number_of_colors)]) for i in range(number_of_colors)]

def ganttplot(tasks):
    colors = dict()
    for task in tasks:
        color = 'rgb(128, 138, 135)'
        colors[str(task.id)] = color
    colors['delay_time'] = 'rgb(255,153,51)'
    colors['move_time'] = 'rgb(0,204,204)'
    colors['work_time'] = 'rgb(128, 138, 135)'

    df = []
    tasks.sort(key=lambda x: x.start_time + x.delay_time)
    for task in tasks:
        df.append(dict(Task=str(task.id), Start = task.start_time, Finish = task.start_time + task.work_time, Resource=str(task.id)))
        df.append(dict(Task=str(task.id), Start = task.start_time - task.delay_time , Finish = task.start_time , Resource = 'delay_time'))

    fig = ff.create_gantt(df, colors=colors, index_col='Resource', show_colorbar=True, group_tasks=True)
    pp.plot(fig, filename='task-gantt', world_readable=True)

    df = []
    for task in tasks:
        for tug in task.tugs:
            df.append(dict(Task=str(tug.tug_id), Start = task.start_time, Finish = task.start_time + task.work_time, Resource= 'work_time'))
            df.append(dict(Task=str(tug.tug_id), Start = task.start_time - count_move_time(task.task_state, tug.pos, task.start) , Finish = task.start_time, Resource='move_time'))

    fig = ff.create_gantt(df, group_tasks=True, show_colorbar=True , colors=colors, index_col='Resource',showgrid_x=True)
    pp.plot(fig, filename='tug-worktime-gantt', world_readable=True)
