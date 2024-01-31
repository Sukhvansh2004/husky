#!/bin/bash

### CONSTANTS & SETUP ########################################################

SETUP_DIR=$(dirname "$(realpath "${BASH_SOURCE[0]}")")
BASE_SCRIPT_DIR=$(cd -- "$SETUP_DIR/../scripts" && pwd)
ROBOT_SCRIPT_DIR="/home/wanderer/workspace-wanderer/scripts"

ROBOT_NAME="wanderer"
ROBOT_MISSIONS=("autonomy" "es" "ed" "science" "test")
BASE_MISSIONS=("autonomy" "es" "ed" "science" "test" "gui")

LAUNCH_FILE_DIR="$HOME/Desktop/Launch Files/$ROBOT_NAME"
mkdir -p "$LAUNCH_FILE_DIR"

EXEC_TERMINAL_CMD='tty -s || exec gnome-terminal -- $0 "$@"'

### GENERATE SCRIPTS #########################################################

# robot mission scripts
for mission in "${ROBOT_MISSIONS[@]}"
do
	cmd="$ROBOT_SCRIPT_DIR/launch.bash $mission"

	robot_file_path="$LAUNCH_FILE_DIR/${ROBOT_NAME}_${mission}.bash"
	robot_file_contents=$(cat <<- EOF
	#!/bin/bash
	$EXEC_TERMINAL_CMD
	ssh $ROBOT_NAME "$cmd"
	read -p "Press enter to exit"
	EOF
	)
	echo "$robot_file_contents" > "$robot_file_path"
	chmod +x "$robot_file_path"
done

# base station mission scripts
for mission in "${BASE_MISSIONS[@]}"
do
	cmd="$BASE_SCRIPT_DIR/launch.bash $mission"

	base_file_path="$LAUNCH_FILE_DIR/base_${mission}.bash"
	base_file_contents=$(cat <<- EOF
	#!/bin/bash
	$EXEC_TERMINAL_CMD
	$cmd
	read -p "Press enter to exit"
	EOF
	)
	echo "$base_file_contents" > "$base_file_path"
	chmod +x "$base_file_path"
done
