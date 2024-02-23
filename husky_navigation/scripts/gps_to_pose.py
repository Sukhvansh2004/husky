#!/usr/bin/env python

import rospy
from geometry_msgs.msg import PoseStamped
from nav_msgs.msg import Odometry

class OdometryToPoseStamped:
    def __init__(self):
        rospy.init_node('gps_waypoint', anonymous=True)
        self.odom_sub = rospy.Subscriber('/gps_point', Odometry, self.odom_callback)
        self.pose_pub = rospy.Publisher('/move_base_simple/goal', PoseStamped, queue_size=10)

    def odom_callback(self, msg):
        # Extract position and orientation from odometry message
        position = msg.pose.pose.position
        orientation = msg.pose.pose.orientation

        # Create a PoseStamped message
        pose_stamped_msg = PoseStamped()
        pose_stamped_msg.header = msg.header
        pose_stamped_msg.pose.position = position
        pose_stamped_msg.pose.position.z = 0
        pose_stamped_msg.pose.orientation = orientation

        # Publish the PoseStamped message
        self.pose_pub.publish(pose_stamped_msg)

if __name__ == '__main__':
    try:
        odom_to_posestamped = OdometryToPoseStamped()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
