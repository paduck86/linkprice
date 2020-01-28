#FROM ubuntu:16.04
#
## Install dependencies and create dirs
#RUN apt-get -qq update && apt-get install -y python3 \
#                python3-pip cron supervisor --allow-unauthenticated\
#    && rm -rf /var/lib/apt/lists/* \
#    && alias python='python3' \
#    && alias pip='pip3' \
#    && pip3 install --upgrade pip
#
#RUN pip3 install python-telegram-bot responses pycoingecko
FROM paduck86/ln-alarm:latest

COPY ./requirements.txt /usr/src/app/requirements.txt
COPY ./cronpy /etc/cron.d/cronpy
COPY configs /usr/src/app/configs
COPY libs /usr/src/app/libs
COPY ./ln-alarm.sh /usr/src/app/ln-alarm.sh

RUN pip3 install -r /usr/src/app/requirements.txt
RUN chmod 644 /etc/cron.d/cronpy
RUN chmod 644 /etc/crontab
RUN chmod 755 /usr/src/app/libs/ln-alarm.py
RUN chmod 755 /usr/src/app/ln-alarm.sh
RUN crontab /etc/cron.d/cronpy

ENV PYTHONPATH /usr/src/app:$PYTHONPATH

CMD ["cron", "-f"]
