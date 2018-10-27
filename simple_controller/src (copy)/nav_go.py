#!/usr/bin/env python

'''
Copyright (c) 2015, Mark Silliman
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
'''

# TurtleBot must have minimal.launch & amcl_demo.launch
# running prior to starting this script
# For simulation: launch gazebo world & amcl_demo prior to run this script

import rospy
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import actionlib
from actionlib_msgs.msg import *
from geometry_msgs.msg import Pose, Point, Quaternion

class GoToPose():
    def __init__(self):

        self.goal_sent = False

	# What to do if shut down (e.g. Ctrl-C or failure)
	rospy.on_shutdown(self.shutdown)
	
	# Tell the action client that we want to spin a thread by default
	self.move_base = actionlib.SimpleActionClient("move_base", MoveBaseAction)
	rospy.loginfo("Wait for the action server to come up")

	# Allow up to 5 seconds for the action server to come up
	self.move_base.wait_for_server(rospy.Duration(5))

    def goto(self, pos, quat):

        # Send a goal
        self.goal_sent = True
	goal = MoveBaseGoal()
	goal.target_pose.header.frame_id = 'map'
	goal.target_pose.header.stamp = rospy.Time.now()
        goal.target_pose.pose = Pose(Point(pos['x'], pos['y'], 0.000),
                                     Quaternion(quat['r1'], quat['r2'], quat['r3'], quat['r4']))

	# Start moving
        self.move_base.send_goal(goal)

	# Allow TurtleBot up to 60 seconds to complete task
	success = self.move_base.wait_for_result(rospy.Duration(60)) 

        state = self.move_base.get_state()
        result = False

        if success and state == GoalStatus.SUCCEEDED:
            # We made it!
            result = True
            rospy.loginfo("Hooray, reached the desired pose,")
            rospy.sleep(1)
        else:
            self.move_base.cancel_goal()
            rospy.loginfo("The base failed to reach the desired pose")
            rospy.sleep(1)

        self.goal_sent = False
        return result

    def shutdown(self):
        if self.goal_sent:
            self.move_base.cancel_goal()
        rospy.loginfo("Stop")
        rospy.sleep(1)


if __name__ == '__main__':
    try:
        rospy.init_node('nav_test', anonymous=False)
        navigator = GoToPose()

        while not rospy.is_shutdown():

            # Customize the following values so they are appropriate for your location
            position = {'x': -0.105732674598, 'y' : 3.2378794055} # position = {'x': 1.22, 'y' : 2.56}
            quaternion = {'r1' : 0.000, 'r2' : 0.000, 'r3' : -0.661922925644, 'r4' : 0.749571904827}
            rospy.loginfo("Go to (%s, %s) pose", position['x'], position['y']) 
            success = navigator.goto(position, quaternion)

            rospy.sleep(3)

            # Customize the following values so they are appropriate for your location
            position = {'x': 0.85, 'y' : 2.43} # position = {'x': 0.831907475474, 'y' : 2.56}
            quaternion = {'r1' : 0.000, 'r2' : 0.000, 'r3' : 0.707, 'r4' : 0.737}
            rospy.loginfo("Go to (%s, %s) pose", position['x'], position['y']) 
            success = navigator.goto(position, quaternion)

            rospy.sleep(3)

            # Customize the following values so they are appropriate for your location
            #position = {'x': 0.0, 'y' : 0.0} # position = {'x': 0.831907475474, 'y' : 2.56}
            #quaternion = {'r1' : 0.000, 'r2' : 0.000, 'r3' : 0.0, 'r4' : 1.0}
            #rospy.loginfo("Go to (%s, %s) pose", position['x'], position['y']) 
            #success = navigator.goto(position, quaternion)

            #rospy.sleep(3)

            # Customize the following values so they are appropriate for your location
            #position = {'x': 0.0, 'y' : 2.85} # position = {'x': 0.831907475474, 'y' : 2.56}
            #quaternion = {'r1' : 0.000, 'r2' : 0.000, 'r3' : 0.707, 'r4' : 0.707}
            #rospy.loginfo("Go to (%s, %s) pose", position['x'], position['y']) 
            #success = navigator.goto(position, quaternion)

            #rospy.sleep(3)

            # Customize the following values so they are appropriate for your location
            #position = {'x': 2.3, 'y' : 2.85} # position = {'x': 0.831907475474, 'y' : 2.56}
            #quaternion = {'r1' : 0.000, 'r2' : 0.000, 'r3' : 1.0, 'r4' : 0.0}
            #rospy.loginfo("Go to (%s, %s) pose", position['x'], position['y']) 
            #success = navigator.goto(position, quaternion)

            #rospy.sleep(3)


            #rospy.spin()

    except rospy.ROSInterruptException:
        rospy.loginfo("Ctrl-C caught. Quitting")

