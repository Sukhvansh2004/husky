# aruco_sim
Spawn Aruco Markers into gazebo and rviz simulations

To add an aruco_marker into a world:

Either have gazebo running or run `$ roslaunch aruco_sim world.launch`

After Gazebo is running the following command spawns markers:

`$ roslaunch aruco_sim arucoSpawner.launch file_name:=arucoMarker##.dae model_name:=%%%%%%`
 
 Where `##` should be replaced by any of the following Aruco Marker ID's:
 
 `0 1 2 3 4 5`
 
 And `%%%%%%` is any unique String name
 
 X, Y, and Z positions can also be set using the parameters:
 
 `x:=##.## y:=##.## x:=##.##`
 
 Where `##.##` is any meter distance as a floating point number

An example is:

`$ roslaunch aruco_sim arucoSpawner.launch file_name:=arucoMarker0.dae model_name:=Marker0 x:=1.00 y:= 1.00 z:=0.00`
