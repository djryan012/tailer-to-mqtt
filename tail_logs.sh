#!/bin/bash

# Use jq to parse YAML file
target_container=$(yq eval '.target_container' /app/config.yaml)
mqtt_broker=$(yq eval '.mqtt_broker' /app/config.yaml)
mqtt_topic=$(yq eval '.mqtt_topic' /app/config.yaml)
mqtt_username=$(yq eval '.mqtt_username' /app/config.yaml)
mqtt_password=$(yq eval '.mqtt_password' /app/config.yaml)

# Extract keywords from the config file
keywords=($(yq eval '.keywords[]' "$config_file"))

# Tail logs, filter specific lines, and publish to MQTT
docker logs -f "$target_container" | while read -r line; do
  for keyword in "${keywords[@]}"; do
    if echo "$line" | grep -q "$keyword"; then
      mosquitto_pub -h "$mqtt_broker" -t "$mqtt_topic" -u "$mqtt_username" -P "$mqtt_password" -m "$line"
      break
    fi
  done
done
