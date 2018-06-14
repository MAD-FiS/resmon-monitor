#!/bin/bash

# Run tests
if [ -z ${RESMONMONITORENV+x} ]; then
    source ./resmon-monitor.env
fi

python3 test/*.py
