FROM osrf/ros:noetic-desktop-full

# update, upgrade, and install packages
RUN apt update \
	&& apt upgrade -y \
	&& apt autoremove -y \
	&& apt install -y apt-utils \
	&& apt install -y software-properties-common \
	&& apt install -y git \
	&& apt install -y iputils-ping \
	&& apt install -y nmap \
	&& apt install -y sudo \
	&& apt install -y udev \
	&& apt install -y tmux \
	&& apt install -y wget \
	&& apt install -y curl \
	&& apt install -y python3-pip \
	&& apt install -y gstreamer1.0-plugins-good

# add urc user
ARG USERNAME=urc
ARG USER_UID=1000
ARG USER_GID=$USER_UID
RUN groupadd --gid $USER_GID $USERNAME \
	&& useradd --shell /bin/bash --uid $USER_UID --gid $USER_GID -m $USERNAME \
	&& echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
	&& chmod 0440 /etc/sudoers.d/$USERNAME \
 	&& echo "export PATH=$PATH:/home/urc/bin" >> /home/urc/.bashrc
WORKDIR /home/urc/workspace-wanderer
USER $USERNAME

# user environment setup
COPY setup/.tmux.conf /home/urc/.tmux.conf
COPY setup/.vimrc /home/urc/.vimrc

# pixhawk geographic libs
RUN sudo apt install -y geographiclib-tools \
	&& sudo wget https://raw.githubusercontent.com/mavlink/mavros/\
master/mavros/scripts/install_geographiclib_datasets.sh -O - | sudo bash

# ros install (removes some things from the base container so the install_noetic.bash script works properly)
COPY setup/install_noetic.bash /build/install_noetic.bash
RUN sudo rm -r /etc/ros/rosdep/sources.list.d \
	&& sudo rm /etc/apt/sources.list.d/ros1-latest.list \
	&& /build/install_noetic.bash \
	&& sudo rm /build/install_noetic.bash \
	&& echo "source /home/urc/workspace-wanderer/devel/setup.bash" >> /home/urc/.bashrc

# install additional rosdep dependencies (rosdep or true so container build doesnt fail)
COPY . /build/build_workspace/
RUN sudo apt update
RUN rosdep install --from-paths /build/build_workspace/src -y --ignore-src || true \
	&& sudo rm -r /build/build_workspace

# install configs
COPY setup/gui_presets/default_presets/* /home/urc/.ros/gui_presets/
COPY setup/autonomy_saves/evansdale/* /home/urc/.ros/autonomy_saves/
COPY setup/autonomy_saves/sim/* /home/urc/.ros/autonomy_saves/
COPY setup/autonomy_saves/test/* /home/urc/.ros/autonomy_saves/
COPY setup/camera_info/realsense/* /home/urc/.ros/camera_info/
COPY setup/camera_info/webcams/* /home/urc/.ros/camera_info/
COPY setup/mission_checklists/checklists/* /home/urc/.ros/mission_checklists/
RUN sudo chown -R urc:urc /home/urc/.ros

# run tmux on startup
CMD tmux
