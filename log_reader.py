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

        accumulated_log = b""  # Accumulate bytes to form a complete log line

        for byte_char in logs:
            char = byte_char.decode('utf-8')

            if char == '\n':
                # End of a log line, print and reset accumulated_log
                print(f"Log Line: {accumulated_log.decode('utf-8').strip()}")
                accumulated_log = b""
            else:
                # Accumulate bytes to form a complete log line
                accumulated_log += byte_char

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
