FROM alpine

WORKDIR /app

COPY monitor_logs.sh /app/

RUN chmod +x /app/monitor_logs.sh

RUN apk add --no-cache mosquitto-clients

# Debugging commands to check file existence and content
RUN ls -l /app
RUN cat /app/monitor_logs.sh

CMD ["/bin/ash", "-c", "/app/monitor_logs.sh"]
