#!/bin/bash

#yell() { echo "$0: $*" >&2; }
#die() { yell "$*"; exit 111; }
#try() { "$@" || die "cannot $*"; }
#set -x
nl='
'
resetColor() {
	printf "\e[39m"
}
turnRed() {
	printf "\e[31m"	
}
turnGreen() {
	printf "\e[32m"	
}
printError() {
	local errorText=$1
	turnRed
	echo $errorText
	resetColor
}
printInfo() {
	turnGreen
	echo $1
	resetColor
}
terminate() {
	exit 1	
}
checkDirExist() {
	local directoryPath=$1
	if [[ -d $directoryPath ]]
	then
		printInfo "Found directory: $directoryPath"
	else
		printError "Can't find mandatory directory: $directoryPath"
		terminate
	fi
}
checkFileExist() {
	local filePath=$1
	if [[ -d $filePath ]]
	then
		printInfo "Found file: $filePath"
	else
		printError "Can't find mandatory file: $filePath"
		terminate
	fi
}

scriptPath="$( cd "$(dirname "$0")" ; pwd -P )"
scriptDir=`dirname $scriptPath`

createApacheVirtualHostsConfig()
{
local apacheSitesConfigFilePath=$1
serverAdminName=MadTeam

guiClientSidePort=80
guiModuleRoot=/
guiModuleWsgiFileName="monitor.wsgi"
guiModuleWsgiPath=$scriptDir'/'$guiModuleWsgiFileName
guiModuleProcessName="gui_side_module"

sensorSidePort=81
sensorModuleRoot=/
sensorModuleWsgiFileName="sensor_receiver.wsgi"
sensorModuleWsgiPath=$scriptDir'/'$sensorModuleWsgiFileName
sensorModuleProcessName="sensor_side_module"

echo "
<VirtualHost *:$guiClientSidePort>
	ServerAdmin $MadTeam
	DocumentRoot /var/www/html
	ErrorLog \${APACHE_LOG_DIR}/error.log
	CustomLog \${APACHE_LOG_DIR}/access.log combined
		done
	WSGIScriptAlias $guiModuleRoot $guiModuleWsgiPath
	WSGIDaemonProcess $guiModuleProcessName display-name=monitor_$guiModuleProcessName
	WSGIProcessGroup $guiModuleProcessName
</VirtualHost>

<VirtualHost *:$sensorSidePort>
	ServerAdmin $MadTeam
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
local isConfiguredTest="<Directory $scriptDir>"

if ! grep -q "$isConfiguredTest" "$apacheConfigFilePath" ; then
echo "
<Directory $scriptDir>
	Options Indexes FollowSymLinks
	AllowOverride None 
	Require all granted
</Directory>
" >> $apacheConfigFilePath
else
	printInfo "Proper config is already in $apacheConfigFilePath"
fi
}

locateApacheFiles() {
local apache2BinaryPath=$1
local matchOnlyValue=".*=\"(.+)\""
local apacheInfoOutput=`$apache2BinaryPath -V 2> /dev/null`

local serverConfigFileNameLine=`echo "$apacheInfoOutput" | grep SERVER_CONFIG_FILE`
if [[ $serverConfigFileNameLine =~ $matchOnlyValue ]]
then
	apacheConfigFileName="${BASH_REMATCH[1]}"
	printInfo "Found apache2 config filename: $apacheConfigFileName"
else
	printError "Cannot determine configFileName from: $apacheInfoOutput"
	terminate
fi

local serverhttpdRootLine=`echo "$apacheInfoOutput" | grep HTTPD_ROOT`
if [[ $serverhttpdRootLine =~ $matchOnlyValue ]]
then
	serverHttpdRootPath="${BASH_REMATCH[1]}"
	printInfo "Found apache2 serverHttpdRootPath: $serverHttpdRootPath"
else
	printError "Cannot determine serverHttpdRootPath from: $apacheInfoOutput"
	terminate
fi

apacheConfigFilePath=$serverHttpdRootPath'/'$apacheConfigFileName
apacheSitesConfigPath=$serverHttpdRootPath'/'"sites-available/"

checkDirExist $apacheSitesConfigPath
}

backupFile() {
	local filePath=$1
	#sed -i 's/^/#/' $filePath
	echo $filePath
	mv -i $filePath $filePath.bak
}

turnFilesBackup() {
	local directoryPath=$1
	echo $directoryPath
	for file in ${directoryPath}*.conf ; do
		echo "dupa"$file
		backupFile $file
	done
}

createApacheConfiguration() {
	apache2Binary=`which apache2` 
	apacheSearchDirectory="/etc"
	siteConfigFileName="monitorConfig.conf"

	if [ -z "$apache2Binary" ] 
	then
		printError "Tried: 'which apache2', but Apache2 not found!"
		terminate
	else
		printInfo "Found apache2 under: $apache2Binary"
	fi

	locateApacheFiles $apache2Binary
	
	PS3="Are you sure you want to append config lines to $apacheConfigFilePath: "
	select option in "Yes" "Exit"; do
		turnRed
		case $option in
			"Yes" ) appendApacheDirPermissions $apacheConfigFilePath && break;;
			"Exit" ) terminate;;
		esac
		resetColor
	done
	resetColor

	#printInfo `ls -la $apacheSitesConfigPath`
	PS3="Are you sure you want to move files as backups in $apacheSitesConfigPath: "
	select option in "Yes" "Exit"; do
		turnRed
		case $option in
			"Yes" ) turnFilesBackup $apacheSitesConfigPath && break;;
			"Exit" ) terminate;;
		esac
		resetColor
	done
	resetColor
	
	printInfo "Site-config file created"
	createApacheVirtualHostsConfig $apacheSitesConfigPath'/'$siteConfigFileName
}

createApacheConfiguration 

