import threading
import sys
import json

class Actions(object) :
    '''
    addAction(json_data) 
        Adds action and its time to actions object. This function is threadsafe and implements locking a threading lock.
        Actions are instance variables and attatched to the object. You must instantiate an Actions object.
        The input string must be serialized json in the following format: {"action":"string", "time":int}
        The function has the following return types:
            -1 - JSONDecodeError - invalid input string format
            -2 - AttributeError - invalid input string format; action should be a string
            -3 - ValueError - invalid input string format; time does not contain any valid number
            -4 - MissingFieldError - invalid input string format; missing action or time field
            -5 - UnhandledError 
             0 - Success - action was successfully added
    getStats()
        Returns the average time to complete each action. This function is threadsafe and implements locking a threading lock.
        Actions are instance variables and attatched to the object. You must instantiate an Actions object. If a thread is currently adding an action this function will wait for its completion before reading. 
        The function will return the average of each action in a serialized json array in the following format:
            [{
                "action":"string",
                "avg":double
            }, ...]

    reset()
        This function resets the actions object.
    '''
    # #Class Vars
    # _actions_map = dict()
    # _average_map = dict()
    # _count_map = dict()
    # #Class Thread Lock
    # _lock = threading.Lock()

    def __init__(self) :
        self._actions_map = dict()
        self._average_map = dict()
        self._count_map = dict()
        self._lock = threading.Lock()

    def addAction(self, json_data) :
        #Convert from serialized json into vars
        try : 
            python_obj = json.loads(json_data)
        except json.decoder.JSONDecodeError :
            return -1 
        try:
            action = python_obj['action'].lower()
        except AttributeError :
            return -2
        try: 
            time = float(python_obj['time'])
        except ValueError :
            return -3
        
        #Ensure both key values are not null, 0 is acceptable for time - could extend to additionally verify no other key/values in input
        if(not action or not str(time)) :
            return -4

        self._lock.acquire()
        try : 
            if action in self._actions_map :
                self._actions_map[action] = self._actions_map[action] + time
                self._count_map[action] = self._count_map[action] + 1
                self._average_map[action] = self._actions_map[action]/self._count_map[action]
            else : 
                self._actions_map[action] = time
                self._count_map[action] = 1
                self._average_map[action] = time
        except :
            #This should never occur
            err = sys.exc_info()[0]
            return -5
        finally :
            self._lock.release()
            return 0

    def getStats(self) :
        if not self._average_map :
            return  ''
        return_list = []
        #Acquire actions thread lock to not read while its being written
        self._lock.acquire()
        try:
            #Convert the dictionary to a list of objects 
            for key, value in self._average_map.items() :
                data = {}
                data["action"] = key
                data["avg"] = value
                return_list.append(data)
        finally: 
            #Release lock after storing in return_list
            self._lock.release()
        
        #convert list of objects to json
        return_string = json.dumps(return_list, separators=(',', ':'))
        return return_string

    def reset(self) :
        self._actions_map.clear()
        self._average_map.clear()
        self._count_map.clear()
        self._lock = threading.Lock()

    # @classmethod
    # def addAction(cls, json_data) :
    #     #Convert from serialized json into vars
    #     try : 
    #         python_obj = json.loads(json_data)
    #     except json.decoder.JSONDecodeError :
    #         return -1 
    #     try:
    #         action = python_obj['action'].lower()
    #     except AttributeError :
    #         return -2
    #     try: 
    #         time = float(python_obj['time'])
    #     except ValueError :
    #         return -3
        
    #     #Ensure both key values are not null, 0 is acceptable for time - could extend to additionally verify no other key/values in input
    #     if(not action or not str(time)) :
    #         # print('Missing inputs')
    #         return -4

    #     cls._lock.acquire()
    #     try : 
    #         if action in cls._actions_map :
    #             cls._actions_map[action] = cls._actions_map[action] + time
    #             cls._count_map[action] = cls._count_map[action] + 1
    #             cls._average_map[action] = cls._actions_map[action]/cls._count_map[action]
    #         else : 
    #             cls._actions_map[action] = time
    #             cls._count_map[action] = 1
    #             cls._average_map[action] = time
    #     except :
    #         #This should never occur
    #         err = sys.exc_info()[0]
    #         return -5
    #     finally :
    #         cls._lock.release()
    #         return 0

    # @classmethod
    # def getStats(cls) :
    #     if not cls._average_map :
    #         return  ''
    #     return_list = []
    #     #Acquire actions thread lock to not read while its being written
    #     cls._lock.acquire()
    #     try:
    #         #Convert the dictionary to a list of objects 
    #         for key, value in cls._average_map.items() :
    #             data = {}
    #             data["action"] = key
    #             data["avg"] = value
    #             return_list.append(data)
    #     finally: 
    #         #Release lock after storing in return_list
    #         cls._lock.release()
        
    #     #convert list of objects to json
    #     return_string = json.dumps(return_list, separators=(',', ':'))
    #     return return_string

    # @classmethod
    # def reset(cls) : 
    #     cls._actions_map.clear()
    #     cls._average_map.clear()
    #     cls._count_map.clear()
    #     cls._lock = threading.Lock()