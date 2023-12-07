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
CONTAINER_NAME_TO_READ = os.getenv("CONTAINER_NAME_TO_READ", "tailing-to-mqtt")  # Specify the container name
KEYWORDS = os.getenv("KEYWORDS", "error").split(",")
MQTT_USERNAME = os.getenv("MQTT_USERNAME", "")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD", "")

def read_container_logs(container_name, mqtt_client):
    client = docker.from_env()
    try:
        container = client.containers.get(container_name)
        logs = container.logs(stream=True, follow=True)
        for log_line in logs:
            decoded_log = log_line.decode('utf-8').strip()
            print(decoded_log)

            # Publish log to MQTT broker
            mqtt_client.publish(MQTT_TOPIC, decoded_log)

            # Check for keywords
            if any(keyword in decoded_log.lower() for keyword in KEYWORDS):
                logger.info(f"Found keyword(s) {KEYWORDS} in the log!")
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
        mqtt_client.loop_start()

        while True:
            try:
                read_container_logs(CONTAINER_NAME_TO_READ, mqtt_client)
            except KeyboardInterrupt:
                logger.info("Log reader stopped.")
                break
            except Exception as e:
                logger.error(f"An error occurred: {str(e)}")

            # Pause for a short time before checking logs again
            time.sleep(5)

    finally:
        mqtt_client.disconnect()
