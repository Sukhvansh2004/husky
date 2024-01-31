systemIP=$(hostname -I | awk '{print $1}')
ROBOT_IP="192.168.1.69"

export ROS_IP=$systemIP
export ROS_HOSTNAME=$ROS_IP
export ROS_MASTER_URI=http://$ROBOT_IP:11311
