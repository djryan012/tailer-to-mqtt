# Dockerfile for Log Tailing Container

FROM alpine:latest

RUN apk add --no-cache \
    mosquitto-clients \
    jq \
    bash

# Install yaml2env
RUN wget https://github.com/kvz/json2env/releases/download/v1.2/yaml2env -O /usr/local/bin/yaml2env && \
    chmod +x /usr/local/bin/yaml2env

COPY tail_logs.sh /usr/local/bin/tail_logs.sh
COPY config.yml /usr/local/bin/config.yml

RUN chmod +x /usr/local/bin/tail_logs.sh

CMD ["/usr/local/bin/tail_logs.sh"]
