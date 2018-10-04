FROM python:3-alpine
LABEL maintainer="Benji Visser <benny@noqcks.io>"

WORKDIR /usr/src/app/

COPY engine.json /
COPY run.py ./
RUN pip3 install bandit

RUN adduser -u 9000 app -D
USER app

VOLUME /code
WORKDIR /code

CMD ["python", "/usr/src/app/run.py"]
