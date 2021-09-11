#! /bin/bash

APP=karting-api
IMG=qoollo-karting/tracks-api
HOST_PORT=8002
DOCKER_PORT=8080

docker build -t $IMG /home/devops/$APP

for container_id in $(docker ps --filter name=$APP -q)
do
    echo "Stoped container: $container_id"
    docker stop $container_id
done

docker run --rm -td --name $APP -p $HOST_PORT:$DOCKER_PORT $IMG
