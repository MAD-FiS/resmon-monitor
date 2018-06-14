FROM debian:latest

WORKDIR /app

RUN apt-get update

ADD ./install-monitor.sh /app

RUN /app/install-monitor.sh --quiet

CMD /app/resmon-monitor && /bin/bash

EXPOSE 81
EXPOSE 82

ENV TZ=Poland
ENV NAME World
