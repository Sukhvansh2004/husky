#!/usr/bin/env python

import rospy
from geometry_msgs.msg import PoseStamped, Twist
from nav_msgs.msg import Odometry
import math

class SpiralWaypointGenerator:
    def __init__(self):
        rospy.init_node('spiral_waypoint_generator')

        # Parameters
        self.initial_pose = None
        self.spiral_radius = 1.0  # Adjust this based on your requirement
        self.spiral_distance_increment = 0.1  # Adjust this based on your requirement
        self.threshold_distance = 0.2  # Adjust this based on your requirement
        self.next_pose = None
        # Publishers and Subscribers
        self.waypoint_pub = rospy.Publisher('/output_point', PoseStamped, queue_size=1)
        self.odom_sub = rospy.Subscriber('/odometry/filtered', Odometry, self.odometry_callback)

    def odometry_callback(self, odom):
        if self.initial_pose is None:
            self.initial_pose = odom.pose.pose

        if self.next_pose:
            current_distance = self.calculate_distance(self.next_pose, odom.pose.pose)

            if current_distance < self.threshold_distance:
                next_waypoint = self.calculate_spiral_waypoint(odom.pose.pose)
                # self.publish_waypoint(next_waypoint)
                print("Next forward \n", self.next_pose)
        else:
            next_waypoint = self.calculate_spiral_waypoint(odom.pose.pose)
            # self.publish_waypoint(next_waypoint)
            print("Next first", self.next_pose)
        
    def calculate_distance(self, pose1, pose2):
        x1, y1 = pose1.position.x, pose1.position.y
        x2, y2 = pose2.position.x, pose2.position.y
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    def calculate_spiral_waypoint(self, current_pose):
        current_x, current_y = current_pose.position.x, current_pose.position.y

        angle = math.atan2(current_y - self.initial_pose.position.y, current_x - self.initial_pose.position.x)
        next_x = current_x + self.spiral_distance_increment * math.cos(angle)
        next_y = current_y + self.spiral_distance_increment * math.sin(angle)

        waypoint = PoseStamped()
        waypoint.header.frame_id = 'odom'
        waypoint.pose.position.x = next_x
        waypoint.pose.position.y = next_y
        waypoint.pose.orientation.w = 1.0  # Assuming no rotation needed
        self.next_pose = waypoint.pose
        
        return waypoint

    def publish_waypoint(self, waypoint):
        self.waypoint_pub.publish(waypoint)

if __name__ == '__main__':
    try:
        spiral_generator = SpiralWaypointGenerator()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
