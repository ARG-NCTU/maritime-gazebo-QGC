# build all pkgs in workspaec of ROS
catkin build -w ~/maritime-gazebo-QGC/catkin_ws

# build PX4 simulation-in-the-loop related pkgs
git config --global --add safe.directory /home/arg/maritime-gazebo-QGC/PX4-simulation
git config --global --add safe.directory /home/arg/maritime-gazebo-QGC/PX4-simulation/src/modules/mavlink/mavlink
git config --global --add safe.directory /home/arg/maritime-gazebo-QGC/PX4-simulation/platforms/nuttx/NuttX/nuttx
cd PX4-simulation && ./Tools/setup/ubuntu.sh --no-sim-tools --no-nuttx
DONT_RUN=1 make px4_sitl_default gazebo
cd ..