FROM alpine

WORKDIR /app

COPY monitor_logs.sh .

RUN apk add --no-cache mosquitto-clients \
    && chmod +x monitor_logs.sh

CMD ["/bin/sh", "-c", "./monitor_logs.sh"]