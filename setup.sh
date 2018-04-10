#!/bin/bash

function generateWsgiFile {
	currentPath=`pwd`
	wsgiFilename='monitor.wsgi'
	appFiles='swagger_stuff'

	echo "import sys" > $wsgiFilename
	echo "sys.path.insert(0, '$currentPath/$appFiles')" >> $wsgiFilename
	echo "from monitor_main import app as application" >> $wsgiFilename
}

generateWsgiFile


