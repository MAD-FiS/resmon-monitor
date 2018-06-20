# resmon-monitor
Repository for a monitor component, which is part of ResMon software.

**Very important!** The given key file (_./data/jwt.key_) is just used in test environment.
Please, don't use it in your production version!

**Info!** All path existing in this file are considered 
as being used in project/install root directory.

# Usage

```bash
./resmon-monitor [--stop]
```
The optional parameter `--stop` is used if you want to stop monitor services instead of running it.

**Info!** Key file has to be the same as in monitors 
which use this authorization server to confirm identity of users.
You have to generate key and to make sure that both this server and monitor 
use the same version of file.

## Database configuration file

The database configuration file is a JSON file. It contains information about connection
to the MongoDB database which is used by ResMon-monitor.
The file has following fields:

| Name       | Type   | Description                              |
| ---------- |:------:| ---------------------------------------- |
| address    | string | Address where MongoDB is available       |
| port       | string | Port of MongoDB database                 |
| user       | string | Username which is used for authorization |
| password   | string | Password which is used for authorization |

# Instalation

For normal users we provide single file `install-monitor.sh` which is used to install this application.
If you have already downloaded that file, it's enough that you just run it as following:
```bash
./install-monitor.sh --config CONFIG_FILE [--quiet]
```

Configuration file will be copied to internal application directory,
so you can later remove the given file without bad consequences.

Later you have to accept unpacking files (without using opion `--quiet`)
Application will be installed in the same place where script `install-monitor.sh`

## Options
| Option                                 | Default value        | Description                                          |
| -------------------------------------- |:--------------------:| -----------------------------------------------------|
| **--config _CONFIG_FILE_**             | ---                  | Location where is stored JSON configuration file     |
| **--quiet**                            | false                | It's automatically accepted if this option is chosen |

# For developers

**Info!** This instruction is written for developers who use Linux operating system.

You have to clone this repository. Then you can work with it and develop the application.
If you want to run it locally for testing, it doesn't need to create installer `install-monitor.sh`

## Used Python modules

These modules are required by this application. If you want for example run tests,
you need to be sure that all of them are installed on your computer by `pip3`.
You can use for it `./data/requirements` file.

| Module name         | Version      |
| ------------------- |:------------:|
| connexion           | 1.1.15       |
| coverage            | 4.0.3        |
| flask_jwt_extended  | 3.7.2        |
| flask_testing       | 0.6.1        |
| nose                | 1.3.7        |
| pluggy              | 0.3.1        |
| py                  | 1.4.31       |
| pymongo             | 3.6.1        |
| python_dateutil     | 2.6.0        |
| randomize           | 0.13         |
| setuptools          | 21.0.0       |

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
At start you can make yourself sure that the file `install-monitor.sh` 
is created by _build_ script and that it has been executed 
after last changes in your code.

The required step is to run separate Docker container with MongoDB database. 
You can run container with MongoDB by this command:
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