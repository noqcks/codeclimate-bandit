FROM alpine:edge

LABEL maintainer "Benji Visser <benny@noqcks.io>"

WORKDIR /usr/src/app/

COPY engine.json /

RUN apk --update add \
  python2 python3 py2-pip && \
  pip2 install --upgrade pip && \
  pip2 install bandit && \
  mv /usr/bin/bandit /usr/bin/bandit2 && \
  pip3 install --upgrade pip && \
  pip3 install bandit && \
  mv /usr/bin/bandit /usr/bin/bandit3 && \
  rm /var/cache/apk/*

COPY run.py ./

RUN adduser -u 9000 app -D
USER app

VOLUME /code
WORKDIR /code

CMD ["python3", "/usr/src/app/run.py"]
