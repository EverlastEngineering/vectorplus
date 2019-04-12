#!/usr/bin/env python3

import anki_vector
import time
import functools
import datetime
from threading import Event
import foundaface

FoundAFace = foundaface.FoundAFace()

from anki_vector.util import degrees, distance_mm, speed_mmps
from anki_vector.events import Events

class Status:
    is_on_charger = False
    show_is_on_charger = True
    show_are_motors_moving = False

def main():
    def on_robot_observed_face(robot, event_type, event):
        if event.name:
            FoundAFace.takeAction(robot,event.name) 

    def on_robot_state(robot, event_type, event):
        global Status
        
        if robot.status.is_on_charger & Status.show_is_on_charger:
            if Status.is_on_charger != True:
                print("Vector is currently on the charger.")
                # robot.conn.request_control(timeout=5.0)
                # robot.behavior.set_eye_color(0, 0)
                # robot.say_text("On the charger!")
                # robot.conn.release_control()
                Status.is_on_charger = True
        else:
            if Status.is_on_charger != False:
                print("Vector is running off battery power.")
                Status.is_on_charger = False

        if robot.status.are_motors_moving & Status.show_are_motors_moving:
            print("Vector is on the move.")
    
    # Start the an async connection with the robot
    with anki_vector.AsyncRobot(anki_vector.util.parse_command_args().serial, requires_behavior_control=False, default_logging=False) as robot:
        # robot.conn.CONTROL_PRIORITY_LEVEL = 1
        robot.conn.request_control(timeout=5.0)
        robot.say_text("Vector+ 1.0").result()
        robot.conn.release_control()
        # FoundAFace.takeAction(robot,"jason")
        # Subscribe to the on_robot_observed_object event
        on_robot_observed_face = functools.partial(on_robot_observed_face, robot)
        robot.events.subscribe(on_robot_observed_face, Events.robot_observed_face)

        on_robot_state = functools.partial(on_robot_state, robot)
        robot.events.subscribe(on_robot_state, Events.robot_state)

        
        while True: 
            time.sleep(100)

if __name__ == "__main__":
    main()