# aruco_finder
ROS node responsible for publishing coordinates given a ficudial transform
## Description
This ROS node that listens for fiducial transforms from the `aruco_detect`
node, converts to the target coordinate frame, and publishes the
coordinates
