import os
from dotenv import load_dotenv
import time
import docker
from docker.types import LogConfig
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

def get_container_id(container_name):
    client = docker.from_env()
    try:
        project_name = os.getenv("COMPOSE_PROJECT_NAME", "")
        containers = client.containers.list(filters={"name": f"{project_name}_{container_name}"}, all=True)
        if containers:
            return containers[0].id
        else:
            return None
    finally:
        client.close()

def read_container_logs(container_id):
    client = docker.APIClient(base_url='unix://var/run/docker.sock', version='auto', timeout=86400)
    try:
        logs = client.logs(container=container_id, stream=True, follow=True)
        for byte_char in logs:
            char = byte_char.decode('utf-8')
            if char == '\n':
                print(f"Last Log Line: {accumulated_log.strip()}")
                accumulated_log = ""
            else:
                accumulated_log += char
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        raise  # Raising the exception so that it's caught outside the function
    finally:
        client.close()

if __name__ == "__main__":
    try:
        while True:
            container_id = get_container_id(CONTAINER_NAME_TO_READ)
            if container_id:
                read_container_logs(container_id)
            else:
                logger.warning(f"Container '{CONTAINER_NAME_TO_READ}' not found.")
                
            # Pause for a short time before checking logs again
            time.sleep(5)

    except KeyboardInterrupt:
        logger.info("Log reader stopped.")
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
