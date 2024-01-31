#!/bin/bash

parent_path=$(dirname "${BASH_SOURCE[0]}")
workspace_path=$(realpath $parent_path/..)

xhost + > /dev/null
sudo docker run \
-v $workspace_path:/home/urc/workspace-wanderer \
-v /dev/video0:/dev/video0 \
-v /dev/urc:/dev/urc --privileged \
-v /tmp/.X11-unix:/tmp/.X11-unix \
-v ~/.gitconfig:/home/urc/.gitconfig \
-v ~/.ssh/known_hosts:/home/urc/.ssh/known_hosts \
-v ${SSH_AUTH_SOCK}:/home/urc/ssh-auth-sock \
-e SSH_AUTH_SOCK=/home/urc/ssh-auth-sock \
-e DISPLAY=$DISPLAY \
-it --net=host \
-u $(id -u):$(id -g) wvu-urc/wanderer:latest
xhost - > /dev/null
