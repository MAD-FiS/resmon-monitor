#!/bin/bash

# Run tests
if [ -z ${RESMONAUTHENV+x} ]; then
    source ./resmon-auth.env
fi

python3 test/*.py
