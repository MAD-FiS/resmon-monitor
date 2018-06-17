#!/bin/bash

# Run tests
if [ -z ${RESMONMONITORENV+x} ]; then
    source ./resmon-monitor.env
fi

python3.6 -m unittest discover -p "test*.py"
python3.6 -m unittest discover -p "*Test.py"
