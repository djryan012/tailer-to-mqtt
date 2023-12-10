FROM alpine

WORKDIR /app

COPY monitor_logs.sh /app/

RUN chmod +x /app/monitor_logs.sh

RUN apk add --no-cache mosquitto-clients

CMD ["/bin/sh", "-c", "/app/monitor_logs.sh"]
