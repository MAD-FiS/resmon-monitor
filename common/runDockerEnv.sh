#!/bin/bash

#This scripts automates building local docker environment.
#Run script only from project root directory.

scriptPath="$( cd "$(dirname "$0")" ; pwd -P )"

#load common functions
. "$scriptPath/scriptsCommon.sh"

mongoDB="mymongo"

if [ ! "`ls -latr | grep ".monitor-root$"`" ]; then 
    printError "This script can be run only from project root"
    terminate
fi

if [ ! "$(sudo docker ps -q -f name=$mongoDB)" ]; then
    if [ "$(sudo docker ps -aq -f status=exited -f name=$mongoDB)" ]; then
        # cleanup
        sudo docker rm $mongoDB
    fi
    # run  container
    printInfo "Running: sudo docker run --name mymongo -d mongo" &&
    sudo docker run --name $mongoDB -d mongo &&
    printInfo "Success"
fi

printInfo "Running: sudo docker build --file Dockerfile_user -t resmonImage ." &&
sudo docker build --file Dockerfile_user -t resmonimage . && 
printInfo "Success" &&

printInfo "Running: sudo docker run -p 4000:81 -p 4001:82 --link mymongo -it resmonimage" &&
sudo docker run -p 4000:81 -p 4001:82 --link mymongo -it resmonimage && 
printInfo "Good bye!"
