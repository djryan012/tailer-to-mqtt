FROM alpine

WORKDIR /app

COPY monitor_logs.sh .

RUN chmod +x monitor_logs.sh

RUN apk add --no-cache mosquitto-clients

CMD ["/bin/sh", "-c", "./monitor_logs.sh"]