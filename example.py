from algo.estimator import Estimator
from algo.greedy.efficient import efficient_dispatch

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
    print(len(tasks))
    return tasks


def estimate_my_algorithm():
    """
    The basic way to estimate your algorithm
    """
    est = Estimator()
    # determine the output format (default is False, which means only print the summary)
    est.set_print_all(False)
    # est.run(my_dispatch, 100, 120)
    est.run(efficient_dispatch,100,120)
# estimate_example()
estimate_my_algorithm()
