#!/bin/bash

MQTT_HOST=${MQTT_HOST:-"mqtt.eclipse.org"}
MQTT_PORT=${MQTT_PORT:-1883}
MQTT_USERNAME=${MQTT_USERNAME:-""}
MQTT_PASSWORD=${MQTT_PASSWORD:-""}
LOG_KEYWORD=${LOG_KEYWORD:-"Starting Server"}
TARGET_CONTAINER_NAME=${TARGET_CONTAINER_NAME:-"bedrock_creative"}

function on_connect {
    echo "Connected to MQTT Broker"
    mosquitto_pub -h $MQTT_HOST -p $MQTT_PORT -u $MQTT_USERNAME -P $MQTT_PASSWORD -t "log/bedrock" -m "$1"
}

function monitor_logs {
    while true; do
        logs=$(docker logs --tail 1 $TARGET_CONTAINER_NAME 2>/dev/null)
        if [[ $logs == *"$LOG_KEYWORD"* ]]; then
            echo "Matching line found: $logs"
            on_connect "$logs"
        fi
        sleep 1
    done
}

trap 'echo "Exiting..."; exit 0' INT TERM

monitor_logs