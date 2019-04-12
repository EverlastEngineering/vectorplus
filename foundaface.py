import datetime
import time
from anki_vector.util import degrees
from anki_vector.behavior import MIN_HEAD_ANGLE, MAX_HEAD_ANGLE
import vputils

class FoundAFace:
    last_called = datetime.datetime.now()
    functionList = []
    namesCalledOut = []
    waitToStart = 40 # seconds
    noShoutOutToSamePersonFor = 300 # seconds


    def weightedList(self):
        return [
            [self.sayName,8],
            [self.sayBeautiful,2],
            [self.saySoGoodToSeeYou,3]
        ]

    def __init__(self):
        self.functionList = vputils.randomizeListWithWeight(self.weightedList())

    def takeAction(self,robot,name):
        timeDifference = datetime.datetime.now().timestamp() - self.last_called.timestamp()
        
        # don't perform this before x seconds from startup or the last time it was called
        if timeDifference < self.waitToStart:
            return
        
        # if vector has called out someone, don't call out again, unless its been over x seconds
        if name not in self.namesCalledOut or timeDifference > self.noShoutOutToSamePersonFor:
            print("Vector is sending a shoutout to %s" % str(name))
            func = vputils.chooseRandomFunction(self.functionList)
            self.functionList = vputils.reducedFunctionList(self.functionList,func,self)
            self.last_called = datetime.datetime.now()
            self.namesCalledOut.append(name)
            (func)(robot,name)
    
    def sayName(self,robot,name):
        robot.conn.request_control(timeout=5.0)
        robot.say_text("%s! It's me! Vector!" % name).result()
        robot.conn.release_control()

    def sayBeautiful(self,robot,name):
        robot.conn.request_control(timeout=5.0)
        robot.say_text("%s?" % name).result() 
        robot.behavior.set_head_angle(MIN_HEAD_ANGLE)
        robot.say_text("I think you are?").result()
        time.sleep(0.5)
        robot.behavior.set_head_angle(degrees(35))
        robot.say_text("beautiful!").result()
        time.sleep(1.0)
        robot.conn.release_control()
    
    def saySoGoodToSeeYou(self,robot,name):
        robot.conn.request_control(timeout=5.0)
        robot.anim.play_animation('anim_knowledgegraph_success_01')
        robot.say_text("%s! I'm so glad to be your friend!" % name).result()
        robot.anim.play_animation('anim_fistbump_success_01').result()
        robot.conn.release_control()