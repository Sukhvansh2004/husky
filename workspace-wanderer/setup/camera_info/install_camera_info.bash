#!/bin/bash

ros_camera_info=~/.ros/camera_info
mkdir -p $ros_camera_info
cp -f webcams/* $ros_camera_info
cp -f realsense/* $ros_camera_info
