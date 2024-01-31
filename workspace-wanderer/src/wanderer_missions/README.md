# Wanderer Missions Launch Files

## About

This package contains launch files for operating wanderer.

## Conventions

* Files beginning with `base` are intended to be run on a base station laptop
and communicate with wanderer.
* Files beginning with `wanderer` are intended to be run on the wanderer and
communicate with a base station laptop.
* Files beginning with `test` are intended to be run on a base station laptop
and should not communicate with wanderer.

## Pairings

### Missions

Autonomy Mission

* Base Station: `base_autonomy.launch`
* Wanderer: `wanderer_autonomy.launch`
* Purpose: Runs the autonomy mission

### Remote Control

Basic Driving

* Base Station: `base_gamepad.launch` or `base_keyboard.launch`
* Wanderer: `wanderer_drivebase.launch`
* Purpose: Drives the wanderer with no GUI

GUI Driving

* Base Station: `base_gui_gamepad.launch` or `base_gui_keyboard.launch`
* Wanderer: `wanderer_test.launch`
* Purpose: Drives the wanderer with the GUI

### Testing

GUI (base)

* Base Station: `base_gui.launch`
* Wanderer: `wanderer_cameras.launch` or `wanderer_localization.launch`
* Purpose: Test that the GUI can communicate with the cameras and
localization properly

GUI (test)

* Base Station: `test_gui.launch` and `rqt`
* Purpose: Test that the GUI can communicate with the marker manager
and manipulate markers properly

PID Path Planner

* Base Station: `rqt`
* Wanderer: `wanderer_pid_planner.launch`
* Purpose: Test that the pid_path_planner can control the robot properly
by operating it directly using rqt

Autonomy

* Base Station: `test_autonomy.launch` and `rqt`
* Purpose: Test that all of the autonomy nodes communicate properly and the
state machine behaves as expected by operating them using rqt
