#!/bin/bash

scriptPath="$( cd "$(dirname "$0")" ; pwd -P )"

#load configuration file
. "$scriptPath/monitor.conf"

#load common function
. "$scriptPath/../common/scriptsCommon.sh"

scriptDir=`dirname $scriptPath`

#resetColor() {
#    printf "\e[39m"
#}
#turnRed() {
#    printf "\e[31m"
#}
#turnGreen() {
#    printf "\e[32m"
#}
#printError() {
#    local errorText=$1
#    turnRed
#    echo $errorText
#    resetColor
#}
#printInfo() {
#    turnGreen
#    echo $1
#    resetColor
#}
#terminate() {
#    exit 1
#}
#checkDirExist() {
#    local directoryPath=$1
#    if [[ -d $directoryPath ]] ; then
#        printInfo "Found directory: $directoryPath"
#    else
#        printError "Can't find mandatory directory: $directoryPath"
#        terminate
#    fi
#}
#checkFileExist() {
#    local filePath=$1
#    if [[ -f $filePath ]] ; then
#        printInfo "Found file: $filePath"
#    else
#        printError "Can't find mandatory file: $filePath"
#        terminate
#    fi
#}
testConfig() {
    echo $guiModuleWsgiFileName
}
createApacheVirtualHostsConfig() {
    local apacheSitesConfigFilePath=$1

    guiModuleWsgiPath=$scriptPath'/'$guiModuleWsgiFileName
    sensorModuleWsgiPath=$scriptPath'/'$sensorModuleWsgiFileName

echo "
<VirtualHost *:$guiClientSidePort>
    ServerAdmin $serverAdminName
    DocumentRoot /var/www/html
    ErrorLog \${APACHE_LOG_DIR}/error.log
    CustomLog \${APACHE_LOG_DIR}/access.log combined
    WSGIScriptAlias $guiModuleRoot $guiModuleWsgiPath
    WSGIDaemonProcess $guiModuleProcessName display-name=monitor_$guiModuleProcessName
    WSGIProcessGroup $guiModuleProcessName
    WSGIPAssAuthorization On

    RewriteEngine On
    RewriteCond %{REQUEST_METHOD} OPTIONS
    RewriteRule ^(.*)$ $1 [R=200,L]

    Header always set Access-Control-Allow-Origin '*'
    Header always set Access-Control-Allow-Headers 'Content-Type,Accept,Origin,Authorization'
    Header always set Access-Control-Allow-Methods 'GET,POST,PUT,DELETE,OPTIONS'
</VirtualHost>

<VirtualHost *:$sensorSidePort>
    ServerAdmin $serverAdminName
    DocumentRoot /var/www/html
    ErrorLog \${APACHE_LOG_DIR}/error.log
    CustomLog \${APACHE_LOG_DIR}/access.log combined

    WSGIScriptAlias $sensorModuleRoot $sensorModuleWsgiPath
    WSGIDaemonProcess $sensorModuleProcessName display-name=monitor_$sensorModuleProcessName
    WSGIProcessGroup $sensorModuleProcessName
</VirtualHost>
" > $apacheSitesConfigFilePath
}

appendApacheDirPermissions() {
    local apacheConfigFilePath=$1
    local isConfiguredTest="<Directory $scriptPath>"

    if ! grep -q "$isConfiguredTest" "$apacheConfigFilePath" ; then
echo "
<Directory $scriptPath>
    Options Indexes FollowSymLinks
    AllowOverride None
    Require all granted
</Directory>
" >> $apacheConfigFilePath
    else
        printInfo "Proper config is already in $apacheConfigFilePath"
    fi
}
appendApacheListeningPorts() {
    local apacheConfigFilePath=$1
    local portNumber=$2

    local isPortConfiguredLine="Listen $portNumber"
    if ! grep -q "$isPortConfiguredLine" "$apacheConfigFilePath" ; then
echo "
$isPortConfiguredLine
" >> $apacheConfigFilePath
    else
        printInfo "Proper port $portNumber config is already in $apacheConfigFilePath"
    fi
}

locateApacheFiles() {
    #For some reason on docker container, apache2 binary with -V option returns nothing.
    #So the hack is to append "ctl" string to use apach2ctl binary instead.
    #Looks like this have something to do with environmental variables
    local properApacheBinarySuffix="ctl"

    local apache2BinaryPath=$1$properApacheBinarySuffix

    local matchOnlyValue=".*=\"(.+)\""
    local apacheInfoOutput=`$apache2BinaryPath -V 2> /dev/null`

    local serverConfigFileNameLine=`echo "$apacheInfoOutput" | grep SERVER_CONFIG_FILE`
    if [[ $serverConfigFileNameLine =~ $matchOnlyValue ]] ; then
        apacheConfigFileName="${BASH_REMATCH[1]}"
        printInfo "Found apache2 config filename: $apacheConfigFileName"
    else
        printError "Cannot determine configFileName from: $apacheInfoOutput"
        terminate
    fi

    local serverhttpdRootLine=`echo "$apacheInfoOutput" | grep HTTPD_ROOT`
    if [[ $serverhttpdRootLine =~ $matchOnlyValue ]] ; then
        serverHttpdRootPath="${BASH_REMATCH[1]}"
        printInfo "Found apache2 serverHttpdRootPath: $serverHttpdRootPath"
    else
        printError "Cannot determine serverHttpdRootPath from: $apacheInfoOutput"
        terminate
    fi

    apacheConfigFilePath=$serverHttpdRootPath'/'$apacheConfigFileName
    apacheSitesConfigPath=$serverHttpdRootPath'/'"sites-available/"
    apachePortsConfigPath=$serverHttpdRootPath'/'"ports.conf"

    checkDirExist $apacheSitesConfigPath
    checkFileExist $apacheConfigFilePath
    checkFileExist $apachePortsConfigPath
}

backupFile() {
    local filePath=$1
    mv -i $filePath $filePath.bak
}

turnFilesBackup() {
    local directoryPath=$1
    for file in ${directoryPath}*.conf ; do
        backupFile $file
    done
}

createApacheConfiguration() {
    apache2Binary=`which apache2`
    apacheSearchDirectory="/etc"
    siteConfigFileName="monitorConfig.conf"

    if [ -z "$apache2Binary" ] ; then
        printError "Tried: 'which apache2', but Apache2 not found!"
        terminate
    else
        printInfo "Found apache2 under: $apache2Binary"
    fi

    locateApacheFiles $apache2Binary
    appendApacheDirPermissions $apacheConfigFilePath

    #PS3="Are you sure you want to append config lines to $apacheConfigFilePath: "
    #select option in "Yes" "Exit"; do
    #   turnRed
    #   case $option in
    #       "Yes" ) appendApacheDirPermissions $apacheConfigFilePath && break;;
    #       "Exit" ) terminate;;
    #   esac
    #   resetColor
    #done
    #resetColor
    turnFilesBackup $apacheSitesConfigPath

    #printInfo `ls -la $apacheSitesConfigPath`
    #PS3="Are you sure you want to move files as backups in $apacheSitesConfigPath: "
    #select option in "Yes" "Exit"; do
    #   turnRed
    #   case $option in
    #       "Yes" ) turnFilesBackup $apacheSitesConfigPath && break;;
    #       "Exit" ) terminate;;
    #   esac
    #   resetColor
    #done
    #resetColor 

    createApacheVirtualHostsConfig $apacheSitesConfigPath'/'$siteConfigFileName
    printInfo "Site-config file created"

    appendApacheListeningPorts $apachePortsConfigPath $guiClientSidePort
    appendApacheListeningPorts $apachePortsConfigPath $sensorSidePort
    printInfo "Ports config created"
}

createApacheConfiguration

