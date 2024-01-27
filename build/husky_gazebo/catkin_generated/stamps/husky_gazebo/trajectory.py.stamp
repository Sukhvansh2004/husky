import rospy
from trajectory_msgs.msg import MultiDOFJointTrajectory
from geometry_msgs.msg import Twist

def callback(trajectory_msg):
    # Extract linear and angular velocities from the trajectory message
    linear_velocity = trajectory_msg.points[0].velocities[0].linear
    angular_velocity = trajectory_msg.points[0].velocities[0].angular

    # Create a Twist message
    twist_msg = Twist()
    twist_msg.linear.x = linear_velocity.x
    twist_msg.linear.y = linear_velocity.y
    twist_msg.linear.z = linear_velocity.z
    twist_msg.angular.x = angular_velocity.x
    twist_msg.angular.y = angular_velocity.y
    twist_msg.angular.z = angular_velocity.z

    # Publish the Twist message
    pub.publish(twist_msg)

if __name__ == '__main__':
    rospy.init_node('trajectory_to_twist_converter')
    
    # Subscribe to the trajectory topic
    sub = rospy.Subscriber('/smb/command/trajectory', MultiDOFJointTrajectory, callback)
    
    # Publish the Twist message on cmd_vel topic
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)

    rospy.spin()
