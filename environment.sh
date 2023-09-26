source /opt/ros/melodic/setup.bash 
source $HOME/maritime-gazebo-QGC/catkin_ws/devel/setup.bash
export ROS_PACKAGE_PATH=${ROS_PACKAGE_PATH}:~/maritime-gazebo-QGC/PX4-simulation
. ~/maritime-gazebo-QGC/PX4-simulation/Tools/setup_gazebo.bash ~/maritime-gazebo-QGC/PX4-simulation ~/maritime-gazebo-QGC/PX4-simulation/build/px4_sitl_default