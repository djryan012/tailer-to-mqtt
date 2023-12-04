# Dockerfile for Log Tailing Container

FROM alpine:latest

RUN apk add --no-cache \
    mosquitto-clients \
    jq \
    bash \
    wget

# Install yq
RUN wget https://github.com/mikefarah/yq/releases/download/v4.9.3/yq_linux_amd64 -O /usr/local/bin/yq && \
    chmod +x /usr/local/bin/yq

# Install yaml2env
RUN wget https://github.com/kvz/json2env/releases/download/v1.2/yaml2env -O /usr/local/bin/yaml2env && \
    chmod +x /usr/local/bin/yaml2env

WORKDIR /app

COPY tail_logs.sh /usr/local/bin/tail_logs.sh
COPY config.yml /app/config.yml   # Keep the config file in /app

RUN chmod +x /usr/local/bin/tail_logs.sh

CMD ["/usr/local/bin/tail_logs.sh"]
