# maritime-gazebo-QGC

The repository contains the minimized simulation component for a drone. Before you begin, there are several prerequisites that need to be satisfied.

## Part 1. Prerequisites

### Clone repo
* You must set up ssh-key before cloning([ssh-key tutorial](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent))
* After you finish setting, clone this repo:
```
cd ~
```
```
git clone --recursive git@github.com:ARG-NCTU/maritime-gazebo-QGC.git
```
### Docker setup
* To keep environment variables and paths isolated, you should run all the code within a Docker container. Here is the command you should use:

*  Pull image from DockerHub (suggestion)
```
docker pull argnctu/maritime-gazebo-qgc:ipc-18.04 
```

* You can also build docker locally

```
cd ~/maritime-gazebo-QGC/Docker/ipc_18.04
```
```
source build.sh
```

### Catkin build in docker 

* In PC:
```
cd ~/maritime-gazebo-QGC
```
```
source ipc_run.sh
```
```
source build_all.sh
```

### Download QGC

* QGroundControl (QGC) provides full flight control and mission planning for any MAVLink enabled drone. Its primary goal is ease of use for professional users and developers. [please follow this link and install QGC](https://docs.qgroundcontrol.com/master/en/getting_started/download_and_install.html#ubuntu)

## Part 2. Launch simulation environment and run testing script

* Before you start, make sure you had finished all steps in Prerequisites successfully. 

* Source ipc_run.sh to start docker container, and source ipc_join.sh to join an existing container.

* Source environment.sh every time when you were in docker.

* Available in docker image: argnctu/maritime-gazebo-qgc:ipc-18.04 .


## Terminal 1(In Docker)
* Launch gazebo environment

```
cd ~/maritime-gazebo-QGC
```
```
source environment.sh
```
```
roslaunch vrx_gazebo drone_sizihwan.launch
```

## Terminal 2(In PC)
* Start QGC 

```
cd {THE_DIR_WHERE_QGC_IS_SAVED}
```
```
./QGroundControl.AppImage
```

## Terminal 3(In Docker) 
* Run the testing script
```
cd ~/maritime-gazebo-QGC/tests
```
```
python drone_testing.py
```

## Result
* Please note that QGC is located in Sizihwan, and the drone in Gazebo will perform the following actions when you run the testing script: takeoff, move forward, move backward, move leftward, move rightward, rotate, and then land.