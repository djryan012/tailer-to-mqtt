import os
from dotenv import load_dotenv
import time
import docker
import logging

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

def read_container_logs(container_name):
    client = docker.from_env()
    max_retries = 5  # Maximum number of retries
    retries = 0

    try:
        while True:
            try:
                container = client.containers.get(container_name)
                logs = container.logs(stream=True, follow=True)

                last_log_line = ""  # Store the last encountered log line
                accumulated_log = b""  # Initialize accumulated_log

                for byte_char in logs:
                    char = byte_char.decode('utf-8')

                    if char == '\n':
                        # End of a log line, update last_log_line
                        last_log_line = accumulated_log.decode('utf-8').strip()
                        accumulated_log = b""
                    else:
                        # Accumulate bytes to form a complete log line
                        accumulated_log += byte_char

                    # Print the last log line
                    if last_log_line:
                        print(f"Last Log Line: {last_log_line}")

                retries = 0  # Reset retry count on successful log retrieval

            except Exception as e:
                retries += 1
                logger.warning(f"An error occurred: {str(e)}. Retrying... (Retry {retries}/{max_retries})")
                time.sleep(5)  # Wait for a few seconds before trying again

            finally:
                time.sleep(1)  # Add a small sleep to avoid high CPU usage

    except KeyboardInterrupt:
        logger.info("Log reader stopped.")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {str(e)}")
    finally:
        client.close()

if __name__ == "__main__":
    read_container_logs(CONTAINER_NAME_TO_READ)
