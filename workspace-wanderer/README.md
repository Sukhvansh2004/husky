# Workspace-Wanderer
This is the main repository for WVU's URC Wanderer Codebase.

# Table of Contents
[Run Mission Software](#run-mission-software)  
[Installation](#installation)  
[Troubleshooting](#troubleshooting)  

# Run Mission Software
__TODO__

# Installation
Ubuntu 20.04 is required as our codebase runs off ROS Noetic.  
Throughout this guide, "$" denotes commands to run in the terminal.
### Pre-Install: SSH Key  
An ssh key for your current machine must be added to your Github account to clone our repositories.  
SSH keys are used for passwordless authentication.  
For more information see https://docs.github.com/en/authentication/connecting-to-github-with-ssh.

* #### Creating an SSH Key
	`$ ssh-keygen`  
	Keep the default file name, add a password if you'd like.  

* #### Adding the SSH key to your Github account
	Go to https://github.com/settings/keys and click "New SSH Key"  
	Title can be anything  
	For Key, copy paste the output of `$ cat ~/.ssh/id_rsa.pub`  

### Clone workspace-wanderer to ~/workspace-wanderer
Install git if not done so already with `$ sudo apt install git` then:  
`$ git clone git@github.com:wvu-urc/workspace-wanderer.git ~/workspace-wanderer`  
* If this is your first time talking to Github on your machine, you will receive a warning saying authenticity cannot be established.  
	Type "yes" and hit enter.

### Install ROS Noetic
The script `install_noetic.bash` located in the same directory as this file will install ROS Noetic onto the current machine.  
It is based off of https://wiki.ros.org/noetic/Installation/Ubuntu with additions for WVU URC specific stuff.  
It is recommended to be familiar with the install guide linked above, as well as WVU URC specific steps in the script, before running it.  
It assumes the current machine is running __Ubuntu 20.04__. It is the only recommended OS for WVU URC.  
The script also assumes you are using __bash__ (default). If you are using zsh, see __TODO_WRITE_ZSH_SECTION__.  

* #### Run the Install script
	`$ cd workspace-wanderer`  
	`$ ./setup/install_noetic.bash`  
	The script will take roughly 10-30 minutes to complete (It installs ~1000 packages among other things)  
	Once the script finishes, it will print out a message saying so.  
	* Please take a moment to read through the script log to see if any errors occured. If an error did occur, see [Troubleshooting](#troubleshooting).  
	* __After the script finishes, run `$ source ~/.bashrc`__
		* If using zsh then read __TODO_WRITE_ZSH_SECTION__ instead.


* #### Clone the other repositores
	`$ vcs import src < repos.yaml`
	Warning: This command can rarely fail due to Github's anti spam protection or poor internet connection (like in ERB 115). If this happens then wait a few minutes and try again. Sometimes it may be required to run `$ git init` if waiting does not fix the problem.

* #### Install URC Dependencies
	In addition to the base ROS Noetic installed above, additional dependencies are needed for URC. These can be installed using rosdep with the command below. Make sure you're still in the workspace-wanderer directory.  
	`$ rosdep install --from-paths src --ignore-src -r -y`

* #### Install Pixhawk Geographic libs
	You'll also need some geographic libraries in order to use the Pixhawk FCU, they can be installed by running the command below to download and run the installer script.  
	`$ sudo wget https://raw.githubusercontent.com/mavlink/mavros/master/mavros/scripts/install_geographiclib_datasets.sh -O - | sudo bash`

* #### Compile the workspace
	While still in workspace-wanderer, run  
	`$ catkin_make -j4`  
	See [Troubleshooting](#troubleshooting) if you receive errors. 
	
* #### Post Install Notes
	* To pull from all repos in src at once, run `$ vcs pull src`  
	* Make sure to install any new dependencies after pulling new commits using the command from "Install URC Dependencies"
	* Remember to recompile after any code change or commit pull (other than Python or launch files)
	* See [Run Mission Software](#run-mission-software) for how to run code.  
	* Check out the official ROS docs for tutorials, examples, and information on how ROS works!  https://wiki.ros.org/Documentation  
	* Don't be discouraged if you accidently break your Noetic install. Everyone does at some point. It's all apart of learning.
	* Visual Studio Code is a good editor you can install with `$ snap install code --classic`


# Troubleshooting
* I'm getting missing dependency errors while compiling, but I know those dependencies are there!  
	* This can sometimes happen due to dependency race conditions, where project A relies on project B, but project A tries to compile before project B is done. 
	* Try running `$ catkin_make -k` twice. This allows cmake to keep building other projects even if one project fails due to an error. The first time will build the dependencies that keep being missed, and the second time should compile the rest of the workspace.
