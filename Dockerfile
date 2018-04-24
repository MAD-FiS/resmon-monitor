FROM debian:latest

RUN apt-get update && apt-get install -y apache2 \
    libapache2-mod-wsgi-py3 \
    build-essential \
    python3 \
    python3-dev \
    python3-pip \
    vim \
 && apt-get clean \
 && apt-get autoremove \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

ADD . /app

COPY ./requirements.txt /app/requirements.txt
RUN pip3 install --trusted-host pypi.python.org -r /app/requirements.txt

RUN pip3 install -e /app/database/

COPY ./apacheSetup.sh /app/apacheSetup.sh
RUN bash /app/apacheSetup.sh

COPY ./setup.sh /app/setup.sh
RUN bash /app/setup.sh

RUN a2ensite monitorConfig.conf
RUN a2dissite 000-default.conf

EXPOSE 81
EXPOSE 82


ENV NAME World


