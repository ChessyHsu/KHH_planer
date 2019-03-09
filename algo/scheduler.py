"""Define Scheduler class
providing algorithms for distributing
"""
from enum import Enum
# from .greedy.basic import greedy_dispatch
from .greedy.efficient import efficient_dispatch
from .settings import CURRENT_METHOD, DISPATCH_METHOD


class Scheduler():
    def __init__(self, method=CURRENT_METHOD):
        self.method = method

    def exec(self, tasks, tugs):
        if self.method == DISPATCH_METHOD.GREEDY:
            return greedy_dispatch(tasks, tugs)
        elif self.method == DISPATCH_METHOD.EFFICIENT: 
            return efficient_dispatch(tasks, tugs)

