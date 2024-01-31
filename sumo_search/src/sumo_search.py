#!/usr/bin/env python3

import random
from math import atan2, cos, sin, pi
from threading import Lock
from copy import deepcopy

import rospy
from std_srvs.srv import Trigger, TriggerRequest, TriggerResponse
from marker_interfacing.msg import ENUMarker
from geometry_msgs.msg import Point

### main #####################################################################

def main():
	SumoSearch().loop()

class SumoSearch:
	def __init__(self) -> None:
		rospy.init_node('sumo_search')

		### local variables ##################################################

		self.marker_lock = Lock()
		self.center = None
		self.radius = None
		self.prev_search_waypoint = None

		### connect to ROS ###################################################

		current_marker_topic = rospy.get_param("~current_marker_topic")
		current_waypoint_topic = rospy.get_param("~current_waypoint_topic")
		publish_search_waypoint_service = rospy.get_param("~publish_search_waypoint_service")

		self.current_marker_sub = rospy.Subscriber(current_marker_topic, ENUMarker, self.current_marker_sub_callback)
		self.current_waypoint_pub = rospy.Publisher(current_waypoint_topic, Point, queue_size=1)
		self.publish_search_waypoint_srv = rospy.Service(publish_search_waypoint_service, Trigger, self.publish_search_waypoint_callback)

		### end init #########################################################
	
	### local functions ######################################################

	def get_next_search_waypoint(self) -> Point:

		# find angle of previous waypoint in search
		x_prev = self.prev_search_waypoint.x
		y_prev = self.prev_search_waypoint.y
		theta_prev = atan2(x_prev, y_prev)

		# generate random angle of next waypoint
		theta_min = (theta_prev + pi/2) % (2 * pi) # must be at least 90 degrees off from previous angle
		theta_random = pi * random.random() # ranomly add 180 degrees
		theta = theta_random + theta_min

		# calculate x and y of next waypoint in relation to center of circle
		x = self.radius * cos(theta)
		y = self.radius * sin(theta)

		return Point(
			self.center.x + x,
			self.center.y + y,
			self.center.z
		)

	### callbacks ############################################################

	def current_marker_sub_callback(self, enu_marker: ENUMarker):
		with self.marker_lock:
			self.center = enu_marker.waypoint_enu
			self.radius = enu_marker.waypoint_error
			self.prev_search_waypoint = self.center

	def publish_search_waypoint_callback(self, _: TriggerRequest):
		response = TriggerResponse()
		response.success = True
		response.message = "Success"

		# check if no marker
		with self.marker_lock:
			center = deepcopy(self.center)
			radius = deepcopy(self.radius)
			prev_search_waypoint = deepcopy(self.prev_search_waypoint)
		if not (center and radius and prev_search_waypoint):
			msg = "Sumo search has no marker! Cannot publish search waypoint!"
			rospy.logwarn(msg)
			response.success = False
			response.message = msg
			return response

		# publish search waypoint
		self.next_search_waypoint = self.get_next_search_waypoint()
		self.current_waypoint_pub.publish(self.next_search_waypoint)
		self.prev_search_waypoint = self.next_search_waypoint
		return response

	### loop #################################################################

	def loop(self):
		rospy.spin()

if __name__ == '__main__':
	main()
