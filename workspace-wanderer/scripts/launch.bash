#!/bin/bash

### INITIAL CONSTANTS ########################################################

SCRIPT_DIR=$(dirname "${BASH_SOURCE[0]}")
WORKSPACE_DIR=$(realpath $SCRIPT_DIR/..)
VALUES_FILEPATH="$SCRIPT_DIR/values.yaml"
ROBOT_IP="192.168.1.69"

### VALIDATE INPUT ###########################################################

all_missions_str=$(yq eval ".missions[]" $VALUES_FILEPATH)
all_missions_arr=($all_missions_str)

usage()
{
	echo "$0 <mission>"
	echo "  * <mission> can be any of"
	for mission in "${all_missions_arr[@]}"
	do
		echo "    * $mission"
	done
}

# check argument count, should only be 1 (mission)
if [ $# -ne 1 ] ; then
	usage
	exit 1
fi

# check valid mission
selected_mission=$(echo "$all_missions_str" | grep -Eow "$1")
if [ -z $selected_mission ] ; then
	usage
	exit 1
fi

### GET SYSTEM INFO ##########################################################

# get current system's hostname and IP
system_hostname=$(hostname)
system_ip=$(hostname -I | awk '{print $1}')
host_info=$(yq eval ".hosts.$system_hostname" $VALUES_FILEPATH)

### VALIDATE IP ##############################################################

echo "Testing IP Address:"
echo "  * IP Address: $system_ip"

if [ $host_info == "null" ] ; then
	echo "  * Host is not recognized. IP Address could not be validated."

	# assume unknown hosts are base station laptops
	launch_location="base"
else
	expected_ip=$(yq eval ".hosts.$system_hostname.ip" $VALUES_FILEPATH)
	if [ "$system_ip" != "$expected_ip" ]; then
		echo "  * $system_hostname has incorrect IP Address. The correct IP should be $expected_ip."
		exit 1
	fi

	echo "  * IP Address check passed."
	launch_location=$(yq eval ".hosts.$system_hostname.location" $VALUES_FILEPATH)
fi

### LAUNCH THE APPROPRIATE SCRIPT ############################################

source "$WORKSPACE_DIR/devel/setup.bash"

export ROS_IP=$system_ip
export ROS_HOSTNAME=$system_ip
export ROS_MASTER_URI=http://$ROBOT_IP:11311

roslaunch wanderer_missions ${launch_location}_${selected_mission}.launch
