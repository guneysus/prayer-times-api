FROM guneysu/python:3.7
RUN pip install gunicorn

COPY dist/prayer_times-0.1.0-py3-none-any.whl /tmp/
RUN pip install /tmp/prayer_times-0.1.0-py3-none-any.whl
# CMD python -m prayer_times

CMD gunicorn prayer_times.web:app --bind=0.0.0.0:8000