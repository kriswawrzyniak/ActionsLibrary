from actions import Actions
import time
import logging 
import random
import sys
import math
import threading
import unittest

from test import Test

def addActionWorker(action, string) :
    r = random.random()
    time.sleep(r)
    returnCode = action.addAction(string)
    # return returnCode

def getStatsWorker(action) :
    r = random.random()
    time.sleep(r)
    returnString = action.getStats() 
    # return returnString

class TestActions(unittest.TestCase) :
    def set_up(self) :
        Actions.reset()

    #addAction
    def test_addAction_invalidString(self) :
        self.set_up()
        #JSON Decode Error
        err = Actions.addAction('')
        self.assertEqual(err, -1)

        err = Actions.addAction('{"action":"jump", "time:1}')
        self.assertEqual(err, -1)

        err = Actions.addAction('{"action":jump, "time":1}')
        self.assertEqual(err, -1)

        err = Actions.addAction('"action":jump, "time":1}')
        self.assertEqual(err, -1)

        #Attribute Error
        err = Actions.addAction('{"action":10, "time": "hey"}')
        self.assertEqual(err, -2)

    def test_addAction_missingInputs(self) :
        self.set_up()
        #Missing input
        err = Actions.addAction('{"action":"", "time":10}')
        self.assertEqual(err, -4)

        #Value Error
        err = Actions.addAction('{"action":"run", "time":""}')
        self.assertEqual(err, -3)

    def test_addAction_verifyAdd(self) :
        self.set_up()
        ret = Actions.addAction('{"action":"jump", "time":100}')
        self.assertEqual(ret, 0)
        ret = Actions.addAction('{"action":"run", "time":75}')
        self.assertEqual(ret, 0)
        ret = Actions.addAction('{"action":"jump", "time":200}')
        self.assertEqual(ret, 0)
        avg = Actions.getStats()
        self.assertEqual(avg, '[{"action":"jump","avg":150.0},{"action":"run","avg":75.0}]')

    def test_addAction_raceCondition(self) :
        self.set_up()
        for i in range(5):
            string = '{"action":"jump", "time":' + str(100 * i) + '}'
            t = threading.Thread(target=addActionWorker, args=(Actions, string))
            t.start()
        main_thread = threading.currentThread()
        for t in threading.enumerate():
            if t is not main_thread:
                t.join()
        avg = Actions.getStats()
        self.assertEqual(avg, '[{"action":"jump","avg":200.0}]' )

    
    #getStats
    def test_getStats_noData(self) :
        self.set_up()
        avg = Actions.getStats()
        self.assertEqual(avg, '')

    # def test_getStats_raceCondition(self) :


if __name__ == '__main__':
    test = Test()
    test.test()
    print(Actions.getStats())
    unittest.main()
