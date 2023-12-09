import subprocess
import os
import time

def monitor_logs(container_name, keywords):
    while True:
        # Get the last log line from the specified container
        command = f"docker logs --tail 1 {container_name}"
        output = subprocess.check_output(command, shell=True, text=True).strip()

        # Check if any keyword is present in the log line
        if any(keyword in output for keyword in keywords):
            # If a match is found, print the line to the console
            print(output)

        time.sleep(1)

if __name__ == "__main__":
    container_name = os.environ.get("MONITORED_CONTAINER", "bedrock_creative")
    keywords = os.environ.get("KEYWORDS", "").split(", ")

    monitor_logs(container_name, keywords)
