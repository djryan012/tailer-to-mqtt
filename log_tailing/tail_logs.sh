#!/bin/sh

while true; do
    keywords=$(yq eval '.keywords' /app/config.yaml)
    container_name=$(yq eval '.container_name' /app/config.yaml)
    topic=$(yq eval '.mqtt_topic' /app/config.yaml)
    mqtt_username=$(yq eval '.mqtt_username' /app/config.yaml)
    mqtt_password=$(yq eval '.mqtt_password' /app/config.yaml)

    docker logs --tail 0 -f "$container_name" | grep --line-buffered "$keywords" | while read -r line; do
        mosquitto_pub -h mqtt-publisher -t "$topic" -u "$mqtt_username" -P "$mqtt_password" -m "$line"
    done
done
