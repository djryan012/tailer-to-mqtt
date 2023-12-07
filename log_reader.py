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
    try:
        container = client.containers.get(container_name)
        logs = container.logs(stream=True, follow=True)

        for log_line in logs:
            decoded_log = log_line.decode('utf-8').strip()

            # Add this print statement to check each log line
            print(f"Log Line: {decoded_log}")

            if not decoded_log:
                continue  # Skip empty log lines

    except docker.errors.NotFound:
        logger.warning(f"Container '{container_name}' not found.")
        raise  # Raising the exception so that it's caught outside the function
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        raise  # Raising the exception so that it's caught outside the function
    finally:
        client.close()

if __name__ == "__main__":
    try:
        read_container_logs(CONTAINER_NAME_TO_READ)
    except KeyboardInterrupt:
        logger.info("Log reader stopped.")
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
