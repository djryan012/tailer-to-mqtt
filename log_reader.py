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
                                # Print the new log line and keywords for debugging
                                print(f"Decoded Log Line: {current_log_line}")
                                print(f"Keywords: {KEYWORDS}")
                                print(f"Keyword Match: {any(keyword in current_log_line.lower() for keyword in KEYWORDS)}")

                                # Uncomment the following lines to publish to MQTT
                                # mqtt_client.connect(MQTT_BROKER_HOST, int(MQT...
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
        logger.error(f"An error occurred: {str(e)}")
    finally:
        client.close()
