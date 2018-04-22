#!/bin/bash

scriptPath="$( cd "$(dirname "$0")" ; pwd -P )"

#load configuration file
. "$scriptPath/monitor.conf"

echo "Script search path: $scriptPath"

function generateWsgiFile {
    local wsgiPointedMainFile=$1
    local wsgiFilename=$2
    local appFilesDir=$3

    wsgiPath=$scriptPath'/'$wsgiFilename

cat > $wsgiPath << EOL
import sys > $wsgiPath
sys.path.insert(0, '$scriptPath/$appFilesDir')
from $wsgiPointedMainFile import app as application
EOL
}

generateWsgiFile $guiModuleMainFile $guiModuleWsgiFileName $guiModuleApplicationFiles
generateWsgiFile $sensorModuleMainFile $sensorModuleWsgiFileName $sensorModuleApplicationFiles

