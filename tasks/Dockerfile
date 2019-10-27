FROM guneysu/python:3.7

WORKDIR /

ADD updater.py /
ADD prayer_times/ /prayer_times/

RUN apk add curl
ADD tasks/requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt
CMD python updater.py
