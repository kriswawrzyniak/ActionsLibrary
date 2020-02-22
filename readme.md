# Python Actions Library 
 
The actions class implements thread safe functions to add actions and track their average times. The class has 3 instance methods: addAction, getStats, and reset. It also has four private instance members _actions_map, _average_map, _count_map, and _lock. The constructor initializes an instance of the class. Threading locks from the python threading library handle thread synchronization. This eases implementation and testing; this limits the access to the data to a single process, threading can be used to manipulate the data concurrently. If data is needed to persist across processes a seperate data store would be necessary; further details are noted in the future considerations section.\
The _actions_map stores each action and its total accumulated time, the _count_map stores each action and the number of times its been added, the _average_map stores the average time of each action. These three members require _lock to be acquired before reading and mutating. Multiple actions objects can be created to store actions seperately. Seperate objects can be manipulated concurrently because the lock is an instance member. There will be no potential race conditions in this case. The library was tested using unittest from the python standard library and tests are contained in actions_test.py.

## Getting Started

The project uses Python3.7 and has no external dependancies, all packages are from the python standard library. A Dockerfile has been included to optionally run the application in a container with python3.7-alpine. It installs any dependacies listed in requirements.txt should any be added in the future.\
To run the tests outside of docker ensure python3.7 is intalled and simply run with the following: 
```
python3 actions_test.py
```
To run the tests with verbose output you can run with the following arguments:
```
python3 -m unittest -v actions_test.py
```
To run the project with docker, build and run the container with the following: 
```
docker build -t myproject .
docker run myproject
```

To use the library in other files in the same directory you can import the class Actions from actions file:
```
from actions import Actions
```
The following libraries from the python standard library are used in the Actions class:
- threading 
- sys
- json

The following libraries from the python standard library are used in the test file:
- threading
- time
- random
- unittest

## Implementation Details
### Class - Actions
| function        | type            | input                                   | output |
| ------------- |:-------------:    | -----                                   | ----:|
| Actions       | constructor       | self: Actions obj                       |Actions: Actions obj|
| addAction     | instanceMethod    | self: Actions obj, string: json_string  |int: error code|
| getStats      | instanceMethod    | self: Actions obj                       |string: json_string|
| reset         | instanceMethod    | self: Actions obj                       |None|

More information on the class can be found in the help string associated with the class. Use the following python command to read the help string after importing the library:
```
help(Actions)
```
#### Constructor 
Creates an Actions object initializing an empty actions list.\
Example usage:
```
actions = Actions()
```
#### Function - addActions
Public Instance Method\
Adds the action to the object, utilizes _lock to control concurrent access.\
The following form of input string is accepted: 
```
{"action":"jump", "time":100}
```
The following are the return values for the function: 
```
-1 - JSONDecodeError - invalid input string format
-2 - AttributeError - invalid input string format; action should be a string
-3 - ValueError - invalid input string format; time does not contain any valid number
-4 - MissingFieldError - invalid input string format; missing action or time field
-5 - UnhandledError 
0 - Success - action was successfully added
```
Example usage:
```
action_string = '{"action":"jump", "time":100}'
actions.addAction(action_string)
```
#### Function - getStats
Public Instance Method\
Gets the serialized json array of the average times for all the actions of that object, utilizes _lock to control concurrent access.\
The function return string is in the following format: 
```
[{
   "action":"string",
   "avg":double
  }, 
...]
```
Example usage: 
```
average_string = actions.getStats()
```
#### Function - reset
Public Instance Method\
Resets the class's members. This will clear all of the dictionaries and create a new instance of _lock.
Example usage:
```
actions.reset()
```
#### Member - _actions_map
Private Instance Member\
Dictionary indexed by action string with accumulative sum of times.
#### Member - _average_map
Private Instance Member\
Dictionary indexed by action string with average times.
#### Member - _count_map
Private Instance Member\
Dictionary indexed by action string with accumulative action additions count.
#### Member - _lock
Private Instance Member\
threading.Lock used to control concurrent access.

##### Note: Python classes do not have access modifiers; the '_' denote private members or functions.
## Testing Detail
Python's unittest library was utilized to create unit tests for the Actions library. Test cases for addAction and getStats were used and include validating the input, validating simple addAction, validating complex addAction, validating concurrent addAction using threads, and validating getStats output.
## Future Considerations
The Actions class stores the data for each action that is added in the object's instance. This will persist across threads spawned from a single process but will not persist across processes. Synchronization is handled by the threading library, so it is not processs-safe. Depending on the use case, a persistant data store may be more useful. Utilizing a relational database and implementing transaction and row locking would be a better implementation for such a use case. Alternatively, a shared memory region could be initialized and utilized by each process. A synchronization method, such as locks, would still be necessary in this case; python multiprocessing library could be used to implement this.

### Author 
**Kris Wawrzyniak** - *Initial work* - [GitHub](https://github.com/kriswawrzyniak)
