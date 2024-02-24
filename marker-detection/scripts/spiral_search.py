#!/usr/bin/env python

import rospy
from geometry_msgs.msg import PoseStamped, Point
from nav_msgs.msg import Odometry
from tf.transformations import quaternion_from_euler
import math

class SpiralWaypointGenerator:
    def __init__(self):
        rospy.init_node('spiral_waypoint_generator', anonymous=True)

        self.threshold_distance = 2
        self.initial_pose = None
        self.spiral_radius = 20
        self.step_increment = 1
        self.waypoints = self.generate_spiral_waypoints()
        self.current_position = None
        
        self.odom_subscriber = rospy.Subscriber('/odometry/filtered', Odometry, self.odom_callback)
        self.goal_publisher = rospy.Publisher('/move_base_simple/goal', PoseStamped, queue_size=10)

    def generate_spiral_waypoints(self):
        waypoints = []
        t = 1
        while t <= self.spiral_radius:
            x = math.cos(t) * t / 2
            y = math.sin(t) * t / 2

            waypoint = PoseStamped()
            waypoint.header.frame_id = 'odom'
            waypoint.pose.position = Point(x, y, 0.0)
            
            tangent_angle = math.atan2(y + t * math.cos(t), x - t * math.sin(t))
            quaternion = quaternion_from_euler(0, 0, tangent_angle)
            waypoint.pose.orientation.x = quaternion[0]
            waypoint.pose.orientation.y = quaternion[1]
            waypoint.pose.orientation.z = quaternion[2]
            waypoint.pose.orientation.w = quaternion[3]

            waypoints.append(waypoint)

            t += self.step_increment 
        
        return waypoints

    def odom_callback(self, odom_msg):
        if(odom_msg.header.stamp.secs != rospy.Time.now().secs):
            return None
        self.current_position = odom_msg.pose.pose.position
        rate = rospy.Rate(2)
        if not self.initial_pose:
            self.initial_pose = self.current_position
            temp = PoseStamped()
            temp.pose.position.x += self.initial_pose.x
            temp.pose.position.y += self.initial_pose.y
            temp.header.frame_id = 'odom'
            temp.header.stamp = rospy.Time.now()
            self.waypoints.insert(0, temp)
        
        rate.sleep()
        if len(self.waypoints) > 0:
            next_waypoint = self.waypoints[0].pose.position

            distance = math.sqrt((self.current_position.x - next_waypoint.x)**2 +
                                 (self.current_position.y - next_waypoint.y)**2)
            
            if distance < self.threshold_distance:
                self.waypoints.pop(0)
                if len(self.waypoints) > 0:
                    goal_msg = self.waypoints[0]
                    goal_msg.pose.position.x += self.initial_pose.x
                    goal_msg.pose.position.y += self.initial_pose.y
                    goal_msg.header.stamp = rospy.Time.now()
                    self.goal_publisher.publish(goal_msg)
        else:
            print("Spiral Search Finished")
            
    def run(self):
        rospy.spin()

if __name__ == '__main__':
    print("Spiral Search Started")
    spiral_generator = SpiralWaypointGenerator()
    spiral_generator.run()
