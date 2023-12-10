FROM alpine

WORKDIR /app

COPY monitor_logs.sh /app/

RUN chmod +x /app/monitor_logs.sh

RUN apk add --no-cache mosquitto-clients

RUN ls -l /app

CMD ["/bin/ash", "-c", "/app/monitor_logs.sh"]
