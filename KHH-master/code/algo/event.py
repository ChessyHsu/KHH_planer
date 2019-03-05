"""All events which calls dispatching algorithm again
"""

from enum import Enum, IntEnum
from model import TASK_STATE, TUG_STATE
# import WorkingTimePredictor

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


    SHIP_TUG_DELAY = 'ship_tug_delay'
    UNIDENTIFIED_DELAY = 'unidentified_delay'
    PIER_DELAY = 'pier_delay'

    MISMATCH = 'mismatch'
    BEFOREHAND = 'beforehand'
    
    ADD_TUG = 'add_tug'


class Ship_Tug_Delay(): #延遲或提早開始
    def __init__(self, task_id, delta_time , task_list):
        self.task_id = task_id
        self.delta_time = delta_time 
        self.task_list = task_list
    
    def handle(self):
        self.modified_task = None
        for task in self.task_list:
            if task.id == self.task_id and task.task_state.value ==  TASK_STATE.PROCESSING_ASSIGNED:
                modified_task = task
                break
        modified_task.start_time += self.delta_time   
        for tug in modified_task.tug:
            tug.next_available_time += self.delta_time                
        return
                                
    def __str__(self):
        return (Event.SHIP_TUG_DELAY)
            

class WorkTimeDelay(): #工作時間預估太早或太晚，結束時間更動

    def __init__(self, task_id, delay_time, task_list):
        self.task_id = task_id
        self.delay_time = delay_time
        self.task_list = task_list
        
    def handle(self):
        modified_task = None
        for task in self.task_list:
            if task.id == self.task_id and task.task_state.value ==  TASK_STATE.PROCESSING_ASSIGNED:
                modified_task = task
                break                

        modified_task.work_time += self.delay_time  
        for tug in modified_task.tug:
            tug.next_available_time += self.delay_time
            
        return
    def __str__(self):
        return(Event.TUG_DELAY)
    
class PierDelay():
    def __init__(self, delta_time, pier, task_list):
        self.delta_time = delta_time
        self.pier = pier
        self.task_list = task_list
        
    def handle(self):
        modified_task = None
        for task in self.task_list:
            if task.to == self.pier and task.task_state.value == TASK_STATE.PROCESSING_ASSIGNED:
                modified_task = task
                break
        if modified_task == None:
            return
        else:
            modified_task.work_time += self.delta_time
            for tug in modified_task.tug:
                tug.next_available_time += self.delta_time
            return
    
    def __str__(self):
        return (Event.PIER_DELAY)

class Mismatch():
    def __init__(self, task_id, required_tug, task_list):
        self.task_id = task_id
        self.required_tug = required_tug
        self.task_list = task_list

    def handle(self):
        for task in self.task_list:
            if task.id == self.task_id and task.task_state.value == TASK_STATE.UNPROCESSED_ASSIGNED:
                self.required_tug.state.value = TUG_STATE.BUSY
                ## ToDo: modify the start time and work time
                # task.start_time =  
                self.required_tug.next_available_time = task.start_time + task.work_time
                task.state.value =  TASK_STATE.PROCESSING
                    

    def __str__(self):
        return (Event.MISMATCH)
    
class Canceled():
    def __init__(self, task_id, task_list):
        self.task_id = task_id
        self.task_list = task_id
    
    def handle(self):
        for task in self.task_list:
            self.task_list.remove(task)            
    
    def __str__(self):
        return (Event.CANCELED)

class AddTug(): #Mismatch的processing版
    def __init__(self,task_id, required_tug, task_list):
        self.task_id = task_id
        self.required_tug = required_tug
        self.task_list = task_list
        
    def handle(self):
        for task in self.task_list:
            if task.id == self.task_id and task.task_state.value == TASK_STATE.PROCESSING_ASSIGNED:
                task.tug_list.append(self.required_tug)
                self.required_tug.state.value == TUG_STATE.BUSY
    
    def __str__(self):
        return (Event.ADD_TUG)