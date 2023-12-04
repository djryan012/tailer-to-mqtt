# Log Tailing Docker Container

This Docker container is designed to tail the logs of another Docker container and publish the tailed results to an MQTT broker. The setup includes a Docker Compose configuration for easy deployment.

## Prerequisites

Before you begin, ensure you have the following:

- Docker installed on your machine.
- Docker Compose installed on your machine.

## Configuration

1. Clone this GitHub repository:

    ```bash
    git clone https://github.com/your-username/log-tailing-docker.git
    cd log-tailing-docker
    ```

2. Edit the `config.yml` file:

    ```yaml
    target_container: "your_target_container_name"
    mqtt_broker: "mqtt://mqtt_broker_address:1883"
    mqtt_topic: "logs"
    mqtt_username: "your_mqtt_username"
    mqtt_password: "your_mqtt_password"
    ```

    Replace the placeholders with your actual container name, MQTT broker details, and authentication credentials.

## Build and Run

Build and run the Docker container using Docker Compose:

```bash
docker-compose build
docker-compose up -d
