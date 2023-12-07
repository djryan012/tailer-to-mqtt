import os
from dotenv import load_dotenv
import time
import docker
import paho.mqtt.client as mqtt
import logging

# Load environmental variables from file
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Retrieve environmental variables
MQTT_BROKER_HOST = os.getenv("MQTT_BROKER_HOST", "mqtt-broker-host")
MQTT_BROKER_PORT = os.getenv("MQTT_BROKER_PORT", "mqtt-broker-port")
MQTT_TOPIC = os.getenv("MQTT_TOPIC", "logs")
CONTAINER_NAME_TO_READ = os.getenv("CONTAINER_NAME_TO_READ")

if CONTAINER_NAME_TO_READ is None:
    raise ValueError("CONTAINER_NAME_TO_READ environment variable not set. Please provide the container name.")

KEYWORDS = os.getenv("KEYWORDS", "error").split(",")
MQTT_USERNAME = os.getenv("MQTT_USERNAME", "")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD", "")

# Print variables for debugging
print(f"MQTT_BROKER_HOST: {MQTT_BROKER_HOST}")
print(f"MQTT_BROKER_PORT: {MQTT_BROKER_PORT}")
print(f"MQTT_TOPIC: {MQTT_TOPIC}")
print(f"CONTAINER_NAME_TO_READ: {CONTAINER_NAME_TO_READ}")  # Corrected variable name
print(f"KEYWORDS: {KEYWORDS}")

def read_container_logs(container_name, mqtt_client):
    client = docker.from_env()
    try:
        container = client.containers.get(container_name)
        logs = container.logs(stream=True, follow=True)
        accumulated_log = ""

        for log_line in logs:
            decoded_log = log_line.decode('utf-8').strip()


            # Add this print statement to check each log line
            print(f"Log Line: {decoded_log}")


            if not decoded_log:
                continue  # Skip empty log lines

            accumulated_log += decoded_log + "\n"

        # Publish accumulated log to MQTT broker
        if accumulated_log.strip():
            # Check for keywords
            if any(keyword in accumulated_log.lower() for keyword in KEYWORDS):
                logger.info(f"Found keyword(s) {KEYWORDS} in the log!")

            # Log the message before publishing
            logger.info(f"Publishing to MQTT: {accumulated_log}")

            mqtt_client.publish(MQTT_TOPIC, accumulated_log)

    except docker.errors.NotFound:
        logger.warning(f"Container '{container_name}' not found.")
        raise  # Raising the exception so that it's caught outside the function
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        raise  # Raising the exception so that it's caught outside the function
    finally:
        client.close()

def on_connect(client, userdata, flags, rc):
    logger.info(f"Connected to MQTT broker with result code {rc}")

if __name__ == "__main__":
    mqtt_client = mqtt.Client()
    mqtt_client.username_pw_set(MQTT_USERNAME, password=MQTT_PASSWORD)
    mqtt_client.on_connect = on_connect

    try:
        mqtt_client.connect(MQTT_BROKER_HOST, int(MQTT_BROKER_PORT), 60)
        mqtt_client.loop_forever()

    except KeyboardInterrupt:
        logger.info("Log reader stopped.")
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
    finally:
        mqtt_client.disconnect()
