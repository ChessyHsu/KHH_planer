import time
from sys import stderr
from .simulator import Simulator
from .his.data import read_data
from .utils.utility import showdetails
from .utils.plot import ganttplot
from algo.greedy.efficient import efficient_dispatch

class Estimator():
    """A class to estimate the given dispatching algorithm

    Attribute:
        print_all: flag to determine if run(algorithm) return detailed state of all tasks

    Method: 
        set_print_all: set output format to return all result or summary
        run: estimates the algorithm with randomly generated events 
    """

    print_all = False

    def set_print_all(self, flag):
        """
        Arg:
            flag (bool): set True to print detailed state of all tasks, False to print summary
            default is to print only the summary of the estimation result
        """
        if flag == True or flag == False:
            self.print_all = flag
        else:
            print("Wrong arguments for set_output. It should only be True or False",
                file=stderr)

    def run(self, algorithm,start_row,end_row):
        """
        Arg:
            algorithm (function): The algorithm as a python function to be estimated

        Return:
            result (str): The result of estimation containing waiting times, tugs, profit, etc
        """
        t_start = time.time()
        event_queue = []
        tasks,tugs,ships = read_data(start_row,end_row)
        simulator = Simulator(event_queue, tasks, tugs, ships, algorithm)
        while simulator.events:
            simulator.run()
        t_end = time.time()
        showdetails(simulator.tasks, algorithm.__name__.upper(), self.print_all)
        print("Time usage: {:.2f} secs".format(t_end - t_start))
        # ganttplot(simulator.tasks)
