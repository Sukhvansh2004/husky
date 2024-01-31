#!/usr/bin/env python3

from threading import Lock

import tf2_ros
import rospy

from std_srvs.srv import Trigger, TriggerRequest, TriggerResponse
from fiducial_msgs.msg import FiducialTransformArray
from geometry_msgs.msg import Point

from aruco_finder.msg import FoundMarker, FoundMarkerList

class ArucoListPublisher:
	def __init__(self) -> None:
		rospy.init_node('aruco_list_publisher')

		self.marker_list_lock = Lock()
		self.marker_list = []
		self.marker_indicies = {}  # aruco_id:list_index

		self.aruco_subs = []

		self.tf_buffer = tf2_ros.Buffer()
		self.tf_listener = tf2_ros.TransformListener(self.tf_buffer)

		found_marker_list = rospy.get_param("~found_marker_list")
		clear_markers_service = rospy.get_param("~clear_markers_service")
		namespace_list = rospy.get_param("~camera_namespaces")
		self.parent_frame = rospy.get_param("~parent_frame")

		self.frequency = rospy.get_param("~frequency")
		fiducial_transform = rospy.get_param("~fiducial_transform")

		# subscribers
		for namespace in namespace_list:
			aruco_sub = rospy.Subscriber(f'/{namespace}/{fiducial_transform}', FiducialTransformArray, self.aruco_callback)
			self.aruco_subs.append(aruco_sub)

		# publishers
		self.marker_list_pub = rospy.Publisher(found_marker_list, FoundMarkerList, queue_size=1)

		self.clear_srv = rospy.Service(clear_markers_service, Trigger, self.clear_markers)

	def lookup_transform(self, child_frame):
		"""lookup child_frame position relative to self.parent_frame"""
		try:
			return self.tf_buffer.lookup_transform(self.parent_frame, child_frame, rospy.Time())
		except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException):
			return None

	def save_marker_position(self, aruco_id, marker_enu):
		found_marker = FoundMarker(marker_enu=marker_enu, aruco_id=aruco_id)

		with self.marker_list_lock:
			if aruco_id in self.marker_indicies:
				# over previous marker entry
				index = self.marker_indicies[aruco_id]
				self.marker_list[index] = found_marker
			else:
				# make new marker entry
				self.marker_indicies[aruco_id] = len(self.marker_list)
				self.marker_list.append(found_marker)

	def aruco_callback(self, fiducial_transform_array: FiducialTransformArray):
		
		for fiducial_transform in fiducial_transform_array.transforms:
			# read marker info
			aruco_id = fiducial_transform.fiducial_id
			child_frame = f'fiducial_{aruco_id}'

			# find marker position relative to parent_frame
			frame_transform = self.lookup_transform(child_frame)
			if frame_transform:
				marker_x = frame_transform.transform.translation.x
				marker_y = frame_transform.transform.translation.y
				marker_z = frame_transform.transform.translation.z
				marker_enu = Point(marker_x, marker_y, marker_z)

				self.save_marker_position(aruco_id, marker_enu)

	def clear_markers(self, _: TriggerRequest) -> TriggerResponse:
		with self.marker_list_lock:
			self.marker_indicies.clear()
			self.marker_list.clear()
		return TriggerResponse(success=True, message='Success')

	def loop(self):
		rate = rospy.Rate(self.frequency)

		while not rospy.is_shutdown():

			marker_count = len(self.marker_list)
			self.marker_list_pub.publish(markers=self.marker_list, count=marker_count)

			rate.sleep()

def main():
	ArucoListPublisher().loop()

if __name__ == '__main__':
	main()
