import threading
import sys
import json

class Actions(object) :
    '''
    static addAction(json_data) 
        Adds action and its time to internal actions data structure. This function is threadsafe and implements locking using a static lock on the Actions class.
        Actions are static and persists through class. No instantiation of the class is needed.
        The input string must be serialized json in the following format: {"action":"string", "time":int}
        The function has the following return types:
            -1 - JSONDecodeError - invalid input string format
            -2 - AttributeError - invalid input string format; action should be a string
            -3 - ValueError - invalid input string format; time does not contain any valid number
            -4 - MissingFieldError - invalid input string format; missing action or time field
            -5 - UnhandledError 
             0 - Success - action was successfully added
    static getStats()
        Returns the average time to complete each action. This function is thread safe and implements locking using a static lock on the Actions class.
        Actions are static and persist through class. No instantiation of the class is needed. If a thread is currently adding and action this function will wait for its completion before reading. 
        The function will return the average of each action in a serialized json array in the following format:
            [{
                "action":"string",
                "avg":double
            }, ...]

    static reset()
        This function resets the internal actions data structure.
    '''
    #Static Vars
    _actions_map = dict()
    _average_map = dict()
    _count_map = dict()
    #Static Thread Lock
    _lock = threading.Lock()

    @staticmethod
    def addAction(json_data) :
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
            # print('Missing inputs')
            return -4

        Actions._lock.acquire()
        try : 
            if action in Actions._actions_map :
                Actions._actions_map[action] = Actions._actions_map[action] + time
                Actions._count_map[action] = Actions._count_map[action] + 1
                Actions._average_map[action] = Actions._actions_map[action]/Actions._count_map[action]
            else : 
                Actions._actions_map[action] = time
                Actions._count_map[action] = 1
                Actions._average_map[action] = time
        except :
            #This should never occur
            err = sys.exc_info()[0]
            return -5
        finally :
            Actions._lock.release()
            return 0
    
    @staticmethod
    def getStats() :
        if not Actions._average_map :
            return  ''
        return_list = []
        #Acquire actions thread lock to not read while its being written
        Actions._lock.acquire()
        try:
            #Convert the dictionary to a list of objects 
            for key, value in Actions._average_map.items() :
                data = {}
                data["action"] = key
                data["avg"] = value
                return_list.append(data)
        finally: 
            #Release lock after storing in return_list
            Actions._lock.release()
        
        #convert list of objects to json
        return_string = json.dumps(return_list, separators=(',', ':'))
        return return_string

    @staticmethod
    def reset() : 
        Actions._actions_map.clear()
        Actions._average_map.clear()
        Actions._count_map.clear()
        Actions._lock = threading.Lock()