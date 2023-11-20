#!/usr/bin/env bash
#
# Typical usage: ./join.bash robotx
#

IMG=argnctu/usv-service:ipc-deploy

xhost +
containerid=$(docker ps -aqf "ancestor=${IMG}") && echo $containerid
docker exec -it \
    --privileged \
    -e DISPLAY=${DISPLAY} \
    -e LINES="$(tput lines)" \
    ${containerid} \
    bash
xhost -
