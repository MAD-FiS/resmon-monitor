#!/bin/bash

# Generates python documentation. Move html files to docs dictionary
if [ -z ${RESMONMONITORENV+x} ]; then
    source ./resmon-monitor.env
fi

rm -rf ./docs
mkdir ./docs/

MODULES=`find -name '*.py' | sed -e 's/\//./g' | sed -e 's/\.\.//g' | sed -e 's/\.py//g' | awk '!/__init__/' | awk '!/__main__/'`
pydoc3 -w $MODULES
for f in ./*.html ; do mv "$f" ./docs/ ; done
