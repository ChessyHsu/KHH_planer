from algo.estimator import Estimator
from algo.greedy.efficient import efficient_dispatch
import time
from algo.predict_worktime import predict_worktime

def estimate_example():
    """
    An example to estimate the build-in efficient-greedy dispatching algorithm
    Take a look at efficient_dispatch() in algo/greedy/efficient.py
    """
    est = Estimator()
    est.set_print_all(True)
    est.run(efficient_dispatch,100,120)
    # est.run(greedy_dispatch)


def my_dispatch(tasks, tugs):
    """
    Implement your own dispatching algorithm
    All algorithms should read tasks and tugs, and modify their states after dispatching
    No return value 
    """
    # dispatch all tasks and modify the state of tasks and tugs
    # print(len(tasks))
    for tug in tugs:
        print(tug)
    for i in tasks:
        print(i)
        if i.id==0:
            t1=time.time()
            work_time = predict_worktime(i, [tugs[4]])
            t2=time.time()
            print("******** %f\n"%(t2-t1))
            print(tugs[4])
            print(work_time)
            print("-----------------------------\n")
    return tasks


def estimate_my_algorithm():
    """
    The basic way to estimate your algorithm
    """
    est = Estimator()
    # determine the output format (default is False, which means only print the summary)
    est.set_print_all(False)
    # est.run(my_dispatch, 100, 120)
    est.run(my_dispatch,100,106)
# estimate_example()
estimate_my_algorithm()
