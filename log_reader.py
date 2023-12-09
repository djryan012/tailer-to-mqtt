import subprocess
import os
from datetime import datetime

def convert_to_datetime(log_timestamp):
    formats = ["%Y-%m-%dT%H:%M:%S.%f", "%Y-%m-%d %H:%M:%S.%f"]
    
    for fmt in formats:
        try:
            return datetime.strptime(log_timestamp, fmt).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]
        except ValueError:
            pass

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

            for log_line in log_lines:
                # Extract timestamp from the log line
                log_timestamp = log_line.split(' ', 1)[0]

                # Convert the timestamp
                converted_timestamp = convert_to_datetime(log_timestamp)

                # Check if any keyword is present in the log line
                if any(keyword in log_line for keyword in keywords):
                    # If a match is found, print the line to the console with the converted timestamp
                    print(f"{converted_timestamp} {log_line}")

        except subprocess.CalledProcessError as e:
            print(f"Error while running 'docker logs': {e}")

        # No sleep, check logs continuously

if __name__ == "__main__":
    container_name = os.environ.get("MONITORED_CONTAINER", "bedrock_creative")
    keywords = os.environ.get("KEYWORDS", "").split(", ")

    monitor_logs(container_name, keywords)
