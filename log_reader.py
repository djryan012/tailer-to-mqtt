import subprocess

def tail_logs(container_name):
    command = f"docker logs --tail 0 -f {container_name}"

    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True)

    try:
        for line in iter(process.stdout.readline, ''):
            line = line.strip()
            print(line)

    except KeyboardInterrupt:
        print("Script terminated by user.")
    finally:
        process.terminate()

if __name__ == "__main__":
    container_name = "bedrock_creative"
    tail_logs(container_name)
