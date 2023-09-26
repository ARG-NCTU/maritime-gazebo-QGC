#!/usr/bin/env bash

IMG=argnctu/maritime-gazebo-qgc:ipc-18.04

xhost +
containerid=$(docker ps -aqf "ancestor=${IMG}")&& echo $containerid
docker exec --privileged -e DISPLAY=${DISPLAY} -e LINES="$(tput lines)" -it ${containerid} bash
xhost -