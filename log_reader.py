import docker

def tail_logs(container_name):
    client = docker.from_env()
    container = client.containers.get(container_name)

    try:
        for line in container.logs(stream=True, follow=True, tail="all"):
            line = line.decode("utf-8").strip()
            print(line)

    except KeyboardInterrupt:
        print("Script terminated by user.")

if __name__ == "__main__":
    container_name = "bedrock_creative"
    tail_logs(container_name)
