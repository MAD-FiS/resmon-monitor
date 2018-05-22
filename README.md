# resmon-monitor
Repository for a monitor component, which is part of resmon product.

# Prerequsites
Before start you have to install Docker CE. Tutorial can be found at:
https://docs.docker.com/install/


# How to run application with docker

First install docker container with mongoDb
```bash
sudo docker run --name myMongo -d mongo
```
Which will download docker container with mongoDb and call it "myMongo".

In directory with monitor project run:
```bash
sudo docker build -t resmonimage .
```
Above command will download and build docker image with all dependencies, environmental configuration 
and will copy application source inside image.


Next you have run :
```bash
sudo docker run -p 4000:81 -p 4001:82 --link myMongo -it resmonimage
```

At this stage you should be done with configuration.


To test the application, run in your OS terminal:
```bash
curl localhost:4001/
```
and

```bash
curl localhost:4000/measurements
```

First command should insert to mongoDb timestamp (this is sensor side), and second should read it from mongoDb. 
You can test this also in your browser.

