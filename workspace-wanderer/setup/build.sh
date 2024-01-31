#!/bin/bash

parent_path=$(dirname "${BASH_SOURCE[0]}")
workspace_path=$(realpath $parent_path/..)

python3 $parent_path/udev_rules/install_udev_rules.py >/dev/null 2>&1

sudo docker build --build-arg USER_UID=$(id -u) --build-arg USER_GID=$(id -g) \
-t wvu-urc/wanderer -f $parent_path/Dockerfile $workspace_path
