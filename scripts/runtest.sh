#!/bin/bash

# Run tests
if [ -z ${RESMONMONITORENV+x} ]; then
    source ./data/resmon-monitor.env
fi

python3.6 -m unittest discover -p "test*.py"
EXIT_CODE1="$?"
python3.6 -m unittest discover -p "*Test.py"
EXIT_CODE2="$?"

if [[ "$EXIT_CODE1" == "0" ]] && [[ "$EXIT_CODE2" == "0" ]]; then
    exit 0
else
    exit 1
fi
