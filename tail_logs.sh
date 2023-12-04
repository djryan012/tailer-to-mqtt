#!/bin/bash

# Load configuration
CONFIG_FILE="/usr/local/bin/config.yml"
if [ ! -f "$CONFIG_FILE" ]; then
  echo "Error: Config file not found!"
  exit 1
fi

eval "$(yaml2env -q "$CONFIG_FILE")"

# Tail logs and publish to MQTT
docker logs -f $target_container | while read -r line; do
  mosquitto_pub -h $mqtt_broker -t $mqtt_topic -u $mqtt_username -P $mqtt_password -m "$line"
done
