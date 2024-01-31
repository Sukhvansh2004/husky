#!/bin/bash

# This script installs ROS Noetic and some WVU URC stuff not handled by rosdep.
# It assumes you are running Ubuntu 20.04.
# The script is based off the ROS Noetic install guide for Ubuntu:
# https://wiki.ros.org/noetic/Installation/Ubuntu

set -e
set -x

# 1. Installation

# 1.1 Configure your Ubuntu repositories
sudo add-apt-repository universe
sudo add-apt-repository multiverse
sudo add-apt-repository restricted

# 1.2 Setup your sources.list
sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'

# 1.3 Set up your keys
sudo apt install curl -y
curl -s https://raw.githubusercontent.com/ros/rosdistro/master/ros.asc | sudo apt-key add -

# 1.4 Installtion
sudo apt update
sudo apt upgrade -y
sudo apt install ros-noetic-desktop-full -y

# 1.5 Environment setup
echo "source /opt/ros/noetic/setup.bash" >> ~/.bashrc
source ~/.bashrc

# 1.6 Dependencies for building packages
sudo apt install python3-rosdep python3-rosinstall python3-rosinstall-generator python3-wstool build-essential -y

# 1.6.1 Initialize rosdep
sudo rosdep init
rosdep update

# 2 WVU URC Specific Stuff

# 2.1 apt packages
sudo add-apt-repository ppa:rmescandon/yq  # yq for parsing launch script
sudo apt install python3-pip python3-vcstool vim htop ros-noetic-tf2-sensor-msgs cmake \
libglfw3-dev libglew-dev libeigen3-dev libjsoncpp-dev libtclap-dev ros-noetic-dynamixel-workbench \
libcap-dev yq libxtst6 -y

# 2.2 pip packages not able to be put in package.xml
python3.8 -m pip install python-prctl pyqtlet2==0.8.0 pyqtgraph==0.11.0 seabreeze

echo "########
########
########
########
ROS NOETIC INSTALLATION COMPLETE
VIEW README.md FOR ADDITIONAL STEPS
########
########
########
########"
