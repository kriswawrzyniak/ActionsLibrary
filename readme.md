# Python Actions Library 
 
This actions class was created to implement thread safe functions to add actions and track their average times. The class has 3 class methods: addAction, getStats, and reset. It also has four private class members _actions_map, _average_map, _count_map, and _lock. These members persist across the class and dont require class instantiation. This was done for ease of implementation and testing; this limits the access to the data to a single process, threading can be used to manipulate the data concurrently, if data is needed to persist across processes a seperate data store would need to be implemented. The _actions_map stores each action and its total accumulated time, the _count_map stores each action and the number of times its been added, the _average_map stores the average time of each action. These three members require _lock to be acquired before reading and mutating. The threading library is used to handle locking and unlocking in the addActions and getStats functions. The library was tested using unittest library and tests are contained in actions_test.py. 

## Getting Started 

The project uses Python3.7 and has no external dependancies, all packages are from the python standard library. A Dockerfile has been included to optionally run the application in a container with python3.7-alpine. It installs any dependacies from requirements.txt should any be added in the future.\
To run the project outside of docker ensure python3.7 is intalled and simply run with the following: 
```
python3 actions_test.py
```

To run the project with docker build and run the container with the following: 
```
docker build -t myproject .
docker run myproject
```

To use the library in other files you can import it the class Actions from actions file:
```
import Actions from actions
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
| addAction     | classMethod       | cls: Actions class, string: json_string |int: error code|
| getStats      | classMethod       | cls: Actions class                      |string: json_string|
| reset         | classMethod       | cls: Actions class                      |None|

More information on the class can be found in the help string associated with the class.
#### Function - addActions
Public Class Method\
Adds the action to the class's members variables, utilizes _lock to control concurrent access.\
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
#### Function - getStats
Public Class Method\
Gets the serialized json array of the average times for all the actions, utilizes _lock to control concurrent access.\
The function return string is in the following format: 
```
[{
   "action":"string",
   "avg":double
  }, 
...]
```
#### Function - reset
Public Class Method\
Resets the class's members, mainly used for testing purposes. This will clear all of the dictionaries and create a new instance of _lock. 
#### Member - _actions_map
Private Class Member\
Dictionary indexed by action string with accumulative sum of times.
#### Member - _average_map
Private Class Member\
Dictionary indexed by action string with average times.
#### Member - _count_map
Private Class Member\
Dictionary indexed by action string with accumulative action additions count.
#### Member - _lock
Private Class Member\
threading.Lock used to control concurrent access.

##### Note: Python classes do not have access modifier; the '_' denote private members or functions.
## Testing Detail
Python's unittest library was utilized to create unit tests for the Actions library. Test cases for addAction and getStats were used and include validating the input, validating simple addAction, validating complex addAction, validating concurrent addAction using threads, and validating getStats output.
## Future Considerations
The Actions class utilizes class member functions to store the data for each action that added. This will persist across threads spawned from a single process but will not persist across processes. Depending on the use case, a persistant data store may be more useful. Utilizing a relational database and implementing transaction and row locking would be a better implementation for such a use case. Alternatively, if the data needed to be shared across processes, a shared memory region could be initialized and utilized by each spawned process. A synchronization method, such as locks, would still be need in this case.

### Author 
**Kris Wawrzyniak** - *Initial work* - [GitHub](https://github.com/kriswawrzyniak)
