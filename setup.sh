#!/bin/bash

scriptPath="$( cd "$(dirname "$0")" ; pwd -P )"

#load configuration file
. "$scriptPath/monitor.conf"


function generateWsgiFile {
    local wsgiPointedMainFile=$1
    local wsgiFilename=$2
    local appFilesDir=$3

    wsgiPath=$scriptPath'/'$wsgiFilename

cat > $wsgiPath << EOL
import sys
sys.path.insert(0, '$scriptPath/$appFilesDir')
from $wsgiPointedMainFile import app as application
EOL
}

echo "Script search path: $scriptPath"
generateWsgiFile $guiModuleMainFile $guiModuleWsgiFileName $guiModuleApplicationFiles
generateWsgiFile $sensorModuleMainFile $sensorModuleWsgiFileName $sensorModuleApplicationFiles

