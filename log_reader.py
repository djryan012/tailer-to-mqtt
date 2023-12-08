import os
from dotenv import load_dotenv
import time
import docker
import logging
import paho.mqtt.client as mqtt
from datetime import datetime, timedelta

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

        # Get logs since the last half hour
        since_time = datetime.now() - timedelta(minutes=30)

        while True:
            try:
                container = client.containers.get(container_name)
                logs = container.logs(stream=True, since=since_time, timestamps=True)

                # Initialize accumulated_log outside the loop
                accumulated_log = b""

                for byte_char in logs:
                    char = byte_char.decode('utf-8')

                    if char == '\n':
                        # End of a log line, check if it's a new log line
                        # Extract the human-readable timestamp from the log line
                        timestamp_start = accumulated_log.find(b'[')
                        timestamp_end = accumulated_log.find(b']', timestamp_start)
                        human_readable_timestamp = accumulated_log[timestamp_start + 1:timestamp_end].decode('utf-8')

                        # Use the human-readable timestamp as the log line
                        current_log_line = f"{human_readable_timestamp} {accumulated_log[timestamp_end + 1:].decode('utf-8').strip()}"

                        accumulated_log = b""

                        # ... (previous code)

                        if current_log_line != last_processed_log_line:
                            print(f"Decoded Log Line: {current_log_line}")

                            # Check for keywords
                            lowercased_line = current_log_line.lower()

                            import re

                            # ...

                            for keyword in KEYWORDS:
                                print(f"Keyword: {keyword}")
                                print(f"Current Log Line (lowercased): {current_log_line}")

                                # Check if the keyword is present anywhere in the log line
                                keyword_match = re.search(r'\b{}\b'.format(re.escape(keyword.lower())), current_log_line.lower())

                                if keyword_match:
                                    print(f"Keyword Match: True for '{current_log_line}'")
                                    # Uncomment the following lines to publish to MQTT
                                    # mqtt_client.connect(MQTT_BROKER_HOST, int(MQT_BROKER_PORT), 60)
                                    # mqtt_client.publish(MQTT_TOPIC, current_log_line)
                                    # mqtt_client.disconnect()

                                    # Update the last processed log line
                                    last_processed_log_line = current_log_line
                                    break
                                else:
                                    print(f"Keyword Match: False for '{current_log_line}'")

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
        logger.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    read_container_logs(CONTAINER_NAME_TO_READ)
