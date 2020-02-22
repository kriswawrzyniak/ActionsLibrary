from actions import Actions
import time
import random
import threading
import unittest


def addActionWorker(action_obj, string) :
    r = random.random()
    time.sleep(r)
    returnCode = action_obj.addAction(string)
    # return returnCode

def getStatsWorker(action_obj) :
    r = random.random()
    time.sleep(r)
    returnString = action_obj.getStats() 
    # return returnString

class TestActions(unittest.TestCase) :
    def set_up(self) :
        self.actions = Actions()
        # Actions.reset()

    #addAction
    def test_addAction_invalidString(self) :
        self.set_up()
        #JSON Decode Error
        err = self.actions.addAction('')
        self.assertEqual(err, -1)

        err = self.actions.addAction('{"action":"jump", "time:1}')
        self.assertEqual(err, -1)

        err = self.actions.addAction('{"action":jump, "time":1}')
        self.assertEqual(err, -1)

        err = self.actions.addAction('"action":jump, "time":1}')
        self.assertEqual(err, -1)

        #Attribute Error
        err = self.actions.addAction('{"action":10, "time": "hey"}')
        self.assertEqual(err, -2)

    def test_addAction_missingInputs(self) :
        self.set_up()
        #Missing input
        err = self.actions.addAction('{"action":"", "time":10}')
        self.assertEqual(err, -4)

        #Value Error
        err = self.actions.addAction('{"action":"run", "time":""}')
        self.assertEqual(err, -3)

    def test_addAction_verifyAdd(self) :
        self.set_up()
        ret = self.actions.addAction('{"action":"jump", "time":100}')
        self.assertEqual(ret, 0)
        ret = self.actions.addAction('{"action":"run", "time":75}')
        self.assertEqual(ret, 0)
        ret = self.actions.addAction('{"action":"jump", "time":200}')
        self.assertEqual(ret, 0)
        avg = self.actions.getStats()
        self.assertEqual(avg, '[{"action":"jump","avg":150.0},{"action":"run","avg":75.0}]')

    def test_addAction_raceCondition(self) :
        self.set_up()
        for i in range(5):
            string = '{"action":"jump", "time":' + str(100 * i) + '}'
            t = threading.Thread(target=addActionWorker, args=(self.actions, string))
            t.start()
        main_thread = threading.currentThread()
        for t in threading.enumerate():
            if t is not main_thread:
                t.join()
        avg = self.actions.getStats()
        self.assertEqual(avg, '[{"action":"jump","avg":200.0}]' )

    
    #getStats
    def test_getStats_noData(self) :
        self.set_up()
        avg = self.actions.getStats()
        self.assertEqual(avg, '')


if __name__ == '__main__':
    unittest.main()
