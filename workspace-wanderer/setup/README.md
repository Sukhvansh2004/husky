# About

This directory provides resources for setting up a development/production
enviornment for the WVU URC wanderer.

# General Resources

* install_noetic.bash: This script installs necessary packages for using ROS
noetic.
* udev_rules: This directory contains udev rules and an installation script.
This allows us to find connected devices at predictable device paths.

# Docker

Running our URC setup in a Docker setup gives a quick, platform agnostic
development environment. This has not been tested well yet.

## Requirements

1. Docker
	* sudo apt install docker
2. VCS Tool
	* Not required for the container, but is required for managing
	workspace repos on the host, which are shared with the container
	* pip install vcstool

Honestly I wasn't documenting the requirements as I went. Anyone else who
uses this PLEASE add details here on requirements/installation commands.

## Build

The build should only need to be run once, or after modifications to the
Dockerfile.

```
./build.sh
```

## Usage

```
./run.sh
```

## Notes

Changes and files inside of the container will not persist.

The workspace is a shared volume meaning those files actually exist on the
host file system and changes are bidirectional.

The entire `/dev` directory is also a shared volume, so devices should come
through to the container.

The container runs with the hosts' networking. There is no isolation.

