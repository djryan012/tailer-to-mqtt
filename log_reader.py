import os
import time
import docker
import paho.mqtt.client as mqtt

MQTT_BROKER_HOST = os.environ.get("MQTT_BROKER_HOST", "mqtt-broker-host")
MQTT_BROKER_PORT = int(os.environ.get("MQTT_BROKER_PORT", 1883))
MQTT_TOPIC = os.environ.get("MQTT_TOPIC", "logs")
CONTAINER_ID_TO_READ = os.environ.get("CONTAINER_ID_TO_READ", "your_container_id")
KEYWORDS = os.environ.get("KEYWORDS", "error").split(",")

MQTT_USERNAME = os.environ.get("MQTT_USERNAME", "")
MQTT_PASSWORD = os.environ.get("MQTT_PASSWORD", "")

def read_container_logs(container_id, mqtt_client):
    client = docker.from_env()
    container = client.containers.get(container_id)
    logs = container.logs(stream=True, follow=True)
    for log_line in logs:
        decoded_log = log_line.decode('utf-8').strip()
        print(decoded_log)

        # Publish log to MQTT broker
        mqtt_client.publish(MQTT_TOPIC, decoded_log)

        # Check for keywords
        if any(keyword in decoded_log.lower() for keyword in KEYWORDS):
            print(f"Found keyword(s) {KEYWORDS} in the log!")

def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT broker with result code {rc}")

if __name__ == "__main__":
    mqtt_client = mqtt.Client()
    mqtt_client.username_pw_set(MQTT_USERNAME, password=MQTT_PASSWORD)
    mqtt_client.on_connect = on_connect

    try:
        mqtt_client.connect(MQTT_BROKER_HOST, MQTT_BROKER_PORT, 60)
        mqtt_client.loop_start()

        while True:
            try:
                read_container_logs(CONTAINER_ID_TO_READ, mqtt_client)
            except docker.errors.NotFound:
                print(f"Container '{CONTAINER_ID_TO_READ}' not found. Retrying in 5 seconds...")
                time.sleep(5)
            except KeyboardInterrupt:
                print("Log reader stopped.")
                break
            except Exception as e:
                print(f"An error occurred: {str(e)}")
                break
    finally:
        mqtt_client.disconnect()
