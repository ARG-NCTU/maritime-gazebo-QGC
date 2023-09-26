source /opt/ros/melodic/setup.bash 
source $HOME/maritime-gazebo-QGC/catkin_ws/devel/setup.bash

export ROS_PACKAGE_PATH=${ROS_PACKAGE_PATH}:~/maritime-gazebo-QGC/PX4-simulation
export GAZEBO_PLUGIN_PATH=$GAZEBO_PLUGIN_PATH:${BUILD_DIR}/build_gazebo
export GAZEBO_MODEL_PATH=$GAZEBO_MODEL_PATH:${SRC_DIR}/Tools/sitl_gazebo/models
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:${BUILD_DIR}/build_gazebo

echo -e "GAZEBO_PLUGIN_PATH $GAZEBO_PLUGIN_PATH"
echo -e "GAZEBO_MODEL_PATH $GAZEBO_MODEL_PATH"
echo -e "LD_LIBRARY_PATH $LD_LIBRARY_PATH"


# ~/maritime-gazebo-QGC/PX4-simulation/Tools/setup_gazebo.bash
# .  ~/maritime-gazebo-QGC/PX4-simulation ~/maritime-gazebo-QGC/PX4-simulation/build/px4_sitl_default