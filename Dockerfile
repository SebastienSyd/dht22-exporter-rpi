FROM arm32v7/python:3-alpine3.12

SHELL ["/bin/sh", "-euxo", "pipefail", "-c"]

WORKDIR /app

RUN \
    apk add --no-cache --virtual .build-deps \
        gcc libc-dev \
    ; \
    apk add --no-cache \
        libgpiod \
    ; \
    pip3 install --no-cache-dir rpi.gpio; \
    pip3 install --no-cache-dir adafruit-circuitpython-dht; \
    pip3 install --no-cache-dir prometheus_client; \
    apk del --no-network --purge .build-deps

COPY main.py ./

RUN chmod +x ./main.py

EXPOSE 9090

CMD ["python3", "-u", "./main.py"]
