import os
from dotenv import load_dotenv
import time
import docker
import logging
import paho.mqtt.client as mqtt

# Load environmental variables from file
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Retrieve environmental variables
CONTAINER_NAME_TO_READ = os.getenv("CONTAINER_NAME_TO_READ")

print(f"CONTAINER_NAME_TO_READ: {CONTAINER_NAME_TO_READ}")
if CONTAINER_NAME_TO_READ is None:
    raise ValueError("CONTAINER_NAME_TO_READ environment variable not set. Please provide the container name.")

# MQTT configuration
MQTT_BROKER_HOST = os.getenv("MQTT_BROKER_HOST", "mqtt-broker-host")
MQTT_BROKER_PORT = os.getenv("MQTT_BROKER_PORT", "mqtt-broker-port")
MQTT_TOPIC = os.getenv("MQTT_TOPIC", "logs")
MQTT_USERNAME = os.getenv("MQTT_USERNAME", "")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD", "")

# Variable to store the last processed log line
last_processed_log_line = ""

# Keywords to check for
KEYWORDS = os.getenv("KEYWORDS", "error").split(",")

def read_container_logs(container_name):
    client = docker.from_env()
    mqtt_client = mqtt.Client()
    mqtt_client.username_pw_set(MQTT_USERNAME, password=MQTT_PASSWORD)

    try:
        # Initialize last_processed_log_line outside the loop
        last_processed_log_line = ""

        while True:
            try:
                container = client.containers.get(container_name)
                logs = container.logs(stream=True, follow=True)

                # Initialize accumulated_log outside the loop
                accumulated_log = b""

                for byte_char in logs:
                    char = byte_char.decode('utf-8')

                    if char == '\n':
                        # End of a log line, check if it's a new log line
                        current_log_line = accumulated_log.decode('utf-8').strip()
                        accumulated_log = b""

                        if current_log_line != last_processed_log_line:
                            # Check for keywords
                            if any(keyword in current_log_line.lower() for keyword in KEYWORDS):
                                # Print the new log line
                                print(f"Last Log Line: {current_log_line}")

                                # Uncomment the following lines to publish to MQTT
                                # mqtt_client.connect(MQTT_BROKER_HOST, int(MQTT_BROKER_PORT), 60)
                                # mqtt_client.publish(MQTT_TOPIC, current_log_line)
                                # mqtt_client.disconnect()

                                # Update the last processed log line
                                last_processed_log_line = current_log_line

                    else:
                        # Accumulate bytes to form a complete log line
                        accumulated_log += byte_char

            except Exception as e:
                logger.warning(f"An error occurred: {str(e)}. Retrying...")
                time.sleep(5)  # Wait for a few seconds before trying again

            finally:
                time.sleep(1)  # Add a small sleep to avoid high CPU usage

    except KeyboardInterrupt:
        logger.info("Log reader stopped.")
    except Exception as e:
        lo
