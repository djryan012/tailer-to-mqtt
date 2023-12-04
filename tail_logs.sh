#!/bin/bash

# Use jq to parse YAML file
target_container=$(yq eval '.target_container' /usr/local/bin/config.yml)
mqtt_broker=$(yq eval '.mqtt_broker' /usr/local/bin/config.yml)
mqtt_topic=$(yq eval '.mqtt_topic' /usr/local/bin/config.yml)
mqtt_username=$(yq eval '.mqtt_username' /usr/local/bin/config.yml)
mqtt_password=$(yq eval '.mqtt_password' /usr/local/bin/config.yml)

# Tail logs, filter specific lines, and publish to MQTT
docker logs -f $target_container | while read -r line; do
  for keyword in "Version" "Starting Server" "Server Started"; do
    if echo "$line" | grep -q "$keyword"; then
      mosquitto_pub -h $mqtt_broker -t $mqtt_topic -u $mqtt_username -P $mqtt_password -m "$line"
      break
    fi
  done
done
