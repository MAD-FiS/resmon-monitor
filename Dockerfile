FROM debian:latest

WORKDIR /app

ADD . /app

RUN ./install-monitor.sh --quiet

CMD /app/resmon-monitor && /bin/bash

EXPOSE 81
EXPOSE 82

ENV TZ=Poland
ENV NAME World
