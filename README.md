# resmon-monitor
Repository for a monitor component, which is part of resmon product.

# Prerequsites
Before you start there is need to install Docker CE. Full tutorial can be found at:
https://docs.docker.com/install/

# How to run application (with docker)

1. Install docker container with mongoDB:
```bash
sudo docker run --name mymongo -d mongo
```
Above command will download docker container with mongoDB and call it "myMongo".

2. In root directory with monitor project run:
```bash
sudo docker build --file Dockerfile_user -t resmonimage .
```
Above command will download and build docker image with all dependencies, environmental configuration 
and will copy application source inside image.

3. Next you have to run container from previously built image :
```bash
sudo docker run -p 4000:81 -p 4001:82 --link mymongo -it resmonimage
```

4. Finally, from container command line start apache2:
```bash
apache2ctl start
```

At this stage you should be done with configuration.

