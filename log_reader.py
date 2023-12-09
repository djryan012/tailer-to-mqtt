import subprocess
import os
from datetime import datetime

def convert_to_datetime(log_timestamp):
    try:
        # Try parsing the timestamp in the first format
        return datetime.strptime(log_timestamp[:30], "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]
    except ValueError:
        raise ValueError(f"Could not parse timestamp: {log_timestamp}")

def monitor_logs(container_name, keywords):
    last_log_timestamp = ""

    while True:
        # Get logs since the last timestamp
        command = f"docker logs --since='{last_log_timestamp}' {container_name}"
        try:
            output = subprocess.check_output(command, shell=True, text=True).strip()

            # Split the output into individual lines
            log_lines = output.splitlines()

            # Update the last log timestamp
            if log_lines:
                last_log_timestamp = convert_to_datetime(log_lines[-1].split(' ', 1)[0])

            # Iterate through each line
            for log_line in log_lines:
                # Check if the log line is not blank
                if log_line.strip():
                    # Check if any keyword is present in the log line
                    if any(keyword in log_line for keyword in keywords):
                        # If a match is found, print the line to the console
                        print(log_line)

        except subprocess.CalledProcessError as e:
            print(f"Error while running 'docker logs': {e}")

        # No sleep, check logs continuously

if __name__ == "__main__":
    container_name = os.environ.get("MONITORED_CONTAINER", "bedrock_creative")
    keywords = os.environ.get("KEYWORDS", "").split(", ")

    monitor_logs(container_name, keywords)
