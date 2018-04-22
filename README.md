# resmon-monitor
Repository for a monitor component, which is part of resmon product.

# Prerequsites
Before start you have to install Docker CE. Tutorial can be found at:
https://docs.docker.com/install/

# How to run application with docker:
In directory with project run:
```bash
sudo docker build -t resmonimage .
```
Above command will download and build docker image with all dependencies, environmental configuration 
and will copy application source inside image.

Then you have to run:
```bash
sudo docker run mongo
```
Which will download docker container with mongoDb.

Next you have to run:
```bash
sudo docker run -p 4000:81 -p 4001:82 --link <mongoDb-containerName> -it resmonimage
```

which will run container in terminal. Then in docker terminal run apache2 server:

In docker terminal run: 
```bash
apache2ctl start
```

To test the application, run in terminal:
```bash
curl localhost:4001/
```
and

```bash
curl localhost:4000/measurements
```

First command will insert to mongoDb timestamp (this is sensor side), and second will read it from mongoDb.

