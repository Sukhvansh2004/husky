import rospy
from rospy import AnyMsg
from std_msgs.msg import String  # For illustrative logging

def callback(data):
    """Logs received data with its topic name and data type."""
    rospy.loginfo("Received data on topic %s of type %s:",
                  data._connection_header['topic'], type(data))

    # Optional: Add logic to extract or process specific data based on type
    if isinstance(data, String):  # Example for String messages
        print(f"Data content: {data.data}")  # Access and print string data

def listener(topic_name):
    """Subscribes to a topic with dynamic data type detection and calls the callback."""
    rospy.init_node(topic_name[1:] + "_listener", anonymous=True)
 	   # topic_type, _, _ = rospy.get_topic_manager(topic_name)  # Dynamic type lookup
    rospy.Subscriber(topic_name, AnyMsg, callback)
    rospy.spin()

if __name__ == '__main__':
	s = """/attached_collision_object 
/cmd_vel 
/collision_object 
/diagnostics
/diagnostics_agg
/diagnostics_toplevel_state
/e_stop
/execute_trajectory/cancel
/execute_trajectory/feedback
/execute_trajectory/goal
/execute_trajectory/result
/execute_trajectory/status
/gps/fix
/head_mount_kinect/depth_registered/points
/husky_velocity_controller/cmd_vel
/husky_velocity_controller/odom
/husky_velocity_controller/parameter_descriptions
/husky_velocity_controller/parameter_updates
/imu/data
/imu_um7/data
/imu_um7/mag
/imu_um7/rpy
/imu_um7/temperature
/joint_states
/joy_teleop/cmd_vel
/joy_teleop/joy
/joy_teleop/joy/set_feedback
/kb_teleop/cmd_vel
/kinova_arm/base_feedback/joint_state
/kinova_arm/in/cartesian_velocity
/kinova_arm/in/clear_faults
/kinova_arm/in/emergency_stop
/kinova_arm/in/joint_velocity
/kinova_arm/in/stop
/kinova_arm/joint_states
/move_group/cancel
/move_group/display_contacts
/move_group/display_planned_path
/move_group/feedback
/move_group/filtered_cloud
/move_group/goal
/move_group/monitored_planning_scene
/move_group/plan_execution/parameter_descriptions
/move_group/plan_execution/parameter_updates
/move_group/planning_pipelines/ompl/ompl/parameter_descriptions
/move_group/planning_pipelines/ompl/ompl/parameter_updates
/move_group/planning_scene_monitor/parameter_descriptions
/move_group/planning_scene_monitor/parameter_updates
/move_group/result
/move_group/sense_for_plan/parameter_descriptions
/move_group/sense_for_plan/parameter_updates
/move_group/status
/move_group/trajectory_execution/parameter_descriptions
/move_group/trajectory_execution/parameter_updates
/odometry/filtered
/odometry/gps
/pickup/cancel
/pickup/feedback
/pickup/goal
/pickup/result
/pickup/status
/place/cancel
/place/feedback
/place/goal
/place/result
/place/status
/planning_scene
/planning_scene_world
/rosout
/rosout_agg
/sequence_move_group/cancel
/sequence_move_group/feedback
/sequence_move_group/goal
/sequence_move_group/result
/sequence_move_group/status
/set_pose
/status
/tf
/tf_static
/trajectory_execution_event
/twist_marker_server/cmd_vel
/twist_marker_server/feedback
/twist_marker_server/update
/twist_marker_server/update_full"""

	for i in s.split():
		listener(i)