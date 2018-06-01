#!/bin/bash

#This script is used to format code of all modified python files, so it conforms
#python PEP8 code standards. To use it, please install "black" program first:
#`pip3 install black`

#Use this script before `git add` command

git status -s | grep '??' | grep '.py' |awk '{print $2}' | xargs black

