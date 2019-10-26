FROM guneysu/python:3.7

WORKDIR /

ADD updater.py /
ADD prayer_times/ /prayer_times/

RUN apk add curl
# CMD curl -vv http://api:8000/api/countries -o /data/countries.json
ADD tasks/requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt
CMD python updater.py
