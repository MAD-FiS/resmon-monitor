# resmon-monitor
Repository for a monitor component, which is part of resmon product.

# Usage

```bash
./resmon-monitor
```

#Instalation
For normal users we provide single file `install-monitor.sh` which is used to install this application.
If you have already downloaded that file, it's enough that you just run it as following:
```bash
./install-monitor.sh [--quiet]
```
Later you have to accept unpacking files. It's automatically accepted if you choose option _--quiet_.
Application will be installed in the same place where script `install-monitor.sh`

#For developers

You have to clone this repository. Then you cna work with it and develop the application.
If you want to run it for testing, it needs to create script `install-monitor.sh` 
with the newest version of code. You can use for it scripts in a way 
which is described below.

## Scripts
You can run some scripts to make your developing process faster and more comfortable.
All scripts can be executed in this way:
```bash
./scripts.sh SCRIPT_NAME
```
where `SCRIPT_NAME` can be as following:
* `build` - it prepares file _install.sh_ to use it later for installing this application
* `docgen` - it generates documentation and puts it into _./docs/_ directory
* `runtest` - it runs all tests available for this project

## Deployment on Docker
You can develop this application on [Docker](https://docs.docker.com). 
It can be used to testing it in a clear environment. 
At start you can make yourself sure that the file `install.sh` is created by _build_ script.

The required step is to run separate Docker container with MongoDB database. 
You can do it by this command:
```bash
docker run --name resmon-monitor-db -d mongo
```

Then you can execute these two following commands:
```bash
docker build --file Dockerfile -t resmon-monitor .
```
and:
```bash
docker run -p 4000:81 -p 4001:82 --link resmon-monitor-db -it resmon-monitor
```
Then you can run there this application. REST API is available on port 4000 
and sensor receiver is running on port 4001.