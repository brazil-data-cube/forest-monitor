FROM forestmonitor/forest-monitor-backend-base:1.0

ADD . /forest-monitor

WORKDIR /forest-monitor

VOLUME /data

CMD [ "python3", "manage.py", "run" ]
