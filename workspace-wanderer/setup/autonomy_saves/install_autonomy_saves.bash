#!/bin/bash

ros_autonomy_saves=~/.ros/autonomy_saves
mkdir -p $ros_autonomy_saves
cp -f evansdale/* $ros_autonomy_saves
cp -f sim/* $ros_autonomy_saves
cp -f test/* $ros_autonomy_saves
