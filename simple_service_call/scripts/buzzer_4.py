#!/usr/bin/env python
'''service_caller ROS Node'''
# license removed for brevity
import rospy
from std_msgs.msg import String
from subprocess import call

def buzzer_4():
    ### $ rosservice call /agc04/test_srv "input: '1111'" ###

    # s = subprocess.call(["rosservice", "call", "/agc04/iocon_srv", "input: '1'"])
    s = call(["rosservice", "call", "/voice_srv", "input: '4'"])
    # print s

if __name__ == '__main__':
    try:
        #iocon_srv_caller()
        
        rospy.init_node('buzzer_4_srv_caller', anonymous=True)

        #while not rospy.is_shutdown():
            
        buzzer_4()

    except rospy.ROSInterruptException:
        pass
