import time
import docker

def read_container_logs(container_id):
    client = docker.from_env()
    container = client.containers.get(container_id)
    logs = container.logs(stream=True, follow=True)
    for log_line in logs:
        print(log_line.decode('utf-8').strip())

if __name__ == "__main__":
    # Replace "your_container_id" with the actual container ID or container name
    container_id_to_read = "your_container_id"
    
    while True:
        try:
            read_container_logs(container_id_to_read)
        except docker.errors.NotFound:
            print(f"Container '{container_id_to_read}' not found. Retrying in 5 seconds...")
            time.sleep(5)
        except KeyboardInterrupt:
            print("Log reader stopped.")
            break
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            break
