import subprocess

keywords = ["Starting Server", "Version"]

def tail_logs(container_name, keywords):
    command = f"docker logs --tail 0 -f {container_name}"

    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True)

    last_lines = {keyword: None for keyword in keywords}

    try:
        for line in iter(process.stdout.readline, ''):
            line = line.strip()
            print(line)

            for keyword in keywords:
                if keyword in line:
                    last_lines[keyword] = line.replace("INFO]", "TRUE]")

            # Check if all keywords have a non-empty last line
            if all(last_lines.values()):
                break

    except KeyboardInterrupt:
        print("Script terminated by user.")
    finally:
        process.terminate()

    for keyword, last_line in last_lines.items():
        if last_line:
            print(f"Last line for keyword '{keyword}': {last_line}")

if __name__ == "__main__":
    container_name = "bedrock_creative"
    tail_logs(container_name, keywords)
