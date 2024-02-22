#!/usr/bin/env python

import rospy
from geometry_msgs.msg import PoseStamped, PointStamped, TransformStamped
import tf2_ros
import tf2_geometry_msgs
from sensor_msgs.msg import NavSatFix

class GPSToPoseStampedConverter:
    def __init__(self):
        rospy.init_node('gps_to_posestamped_converter')

        # Initialize TF buffer and listener
        self.tf_buffer = tf2_ros.Buffer()
        self.tf_listener = tf2_ros.TransformListener(self.tf_buffer)

        # Subscriber to GPS topic
        rospy.Subscriber("/navsat/fix", NavSatFix, self.gps_callback)

        # Publisher for PoseStamped in odom frame
        self.pose_pub = rospy.Publisher("pose_stamped_topic", PoseStamped, queue_size=10)

    def gps_callback(self, gps_msg):
        try:
            # Get transformation from GPS frame to odom frame
            transform = self.tf_buffer.lookup_transform("odom", gps_msg.header.frame_id, rospy.Time())

            # Convert GPS coordinates to PointStamped
            gps_point = PointStamped()
            gps_point.header = gps_msg.header
            gps_point.point.x = gps_msg.longitude
            gps_point.point.y = gps_msg.latitude
            gps_point.point.z = gps_msg.altitude

            # Transform PointStamped to odom frame
            odom_point = tf2_geometry_msgs.do_transform_point(gps_point, transform)

            # Create PoseStamped message
            pose_stamped_msg = PoseStamped()
            pose_stamped_msg.header = odom_point.header
            pose_stamped_msg.pose.position = odom_point.point

            # Publish PoseStamped message
            self.pose_pub.publish(pose_stamped_msg)
        except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException):
            rospy.logwarn("Transformation failed.")

    def run(self):
        rospy.spin()

if __name__ == '__main__':
    gps_converter = GPSToPoseStampedConverter()
    gps_converter.run()
