FROM alpine:3.17.0

LABEL maintainer "Benji Visser <benny@noqcks.io>"

WORKDIR /usr/src/app/

COPY requirements.txt /usr/src/app/

RUN apk add --update \
  python3 py3-pip && \
  pip3 install --upgrade pip && \
  pip3 install -r requirements.txt && \
  mv /usr/bin/bandit /usr/bin/bandit3 && \
  rm /var/cache/apk/*

COPY . /usr/src/app

RUN adduser -u 9000 app -D
USER app

VOLUME /code
WORKDIR /code

CMD ["python3", "/usr/src/app/run.py"]
