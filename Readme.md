# Project Title :

RRT Connect algorithm implemented for a differential drive robot.

# Authors:
1. Badrinarayanan Raghunathan Srikumar - braghuna (119215418)
2. Vyshnav Achuthan - vyachu07 (119304815)


# Dependencies Used:

rospy

math

numpy

pygame

nav_msgs

geometyry_msgs

sys

# Steps to run the code:
1. Unzip the package in your workspace.
2. Run catkin_make
3. To run just the 2D visualization of the algorithm, Please run the rrt_connect_ENPM661.py file using the command "python3 rrt_connect_661.py"
4. To see the gazebo movement for the algorithm, First in a new terminal, launch the file using "roslaunch rrt_connect_ENPM661 turtlebot3_world.launch
5. In another terminal, run the py file in the src folder, using "python3 control.py".
6. If the robot seems to run erratically, please kill both the terminals and run both the files again.


# Default values used for Part 2:
1. Goal : 550,30
2. Start : 50,100

# Video links:
1. https://drive.google.com/file/d/1wQaAvnzt5m-ZCktZzr-gS21sjr8HRcI0/view?usp=share_link
2. https://drive.google.com/file/d/1Mv9Cjfk4DJ1g0I2kJGVleNDnsed8iYcI/view?usp=share_link

# Github link :
https://github.com/Irdab2000/RRT_connect_diffdrive
