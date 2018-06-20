#!/bin/bash

scriptPath="$( cd "$(dirname "$0")" ; pwd -P )"
appPath="$(cd $scriptPath ; cd .. ; pwd -P )"

#load configuration file
. "$scriptPath/monitor.conf"


function generateWsgiFile {
    local wsgiPointedMainFile=$1
    local wsgiFilename=$2

    wsgiPath=$scriptPath'/'$wsgiFilename

cat > $wsgiPath << EOL
import sys
import os
sys.path.insert(0, "$appPath")
from $wsgiPointedMainFile import app as application
EOL
}

echo "Script path: $scriptPath"
echo "App path: $appPath"
generateWsgiFile $guiModuleMainFile $guiModuleWsgiFileName
generateWsgiFile $sensorModuleMainFile $sensorModuleWsgiFileName

