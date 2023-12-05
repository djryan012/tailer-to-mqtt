#!/bin/sh

# Load configuration variables
keywords=$(yq eval '.keywords' /app/config.yml)
container_name=$(yq eval '.container_name' /app/config.yml)
topic=$(yq eval '.mqtt_topic' /app/config.yml)
mqtt_username=$(yq eval '.mqtt_username' /app/config.yml)
mqtt_password=$(yq eval '.mqtt_password' /app/config.yml)

# Display loaded configuration
echo "Log Tailing Container Configuration:"
echo "-------------------------------------"
echo "Keywords: $keywords"
echo "Container Name: $container_name"
echo "MQTT Topic: $topic"
echo "MQTT Username: $mqtt_username"
echo "MQTT Password: ********"

# Log start of the container
echo "Log Tailing Container started at $(date)"

# Tail logs and publish to MQTT
while true; do
    docker logs --tail 0 -f "$container_name" | grep --line-buffered "$keywords" | while read -r line; do
        echo "Found keyword in log: $line"
        mosquitto_pub -h mqtt-publisher -t "$topic" -u "$mqtt_username" -P "$mqtt_password" -m "$line"
    done
done
