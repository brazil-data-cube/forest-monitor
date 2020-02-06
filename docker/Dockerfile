FROM brazildatacube/base:0.1

RUN apt-get update && apt-get install -y build-essential libpq-dev

ADD . /forest-monitor

WORKDIR /forest-monitor

RUN pip3 install -r requirements.txt

VOLUME /data

CMD [ "python3", "manage.py", "run" ]