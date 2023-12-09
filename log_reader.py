import subprocess
import os

def monitor_logs(container_name, keywords):
    last_log_line = ""

    while True:
        # Get all log lines from the specified container
        command = f"docker logs {container_name}"
        try:
            output = subprocess.check_output(command, shell=True, text=True).strip()

            # Split the output into individual lines
            log_lines = output.splitlines()

            # Iterate through each line
            for log_line in log_lines:
                # Check if the log line is not blank and has changed
                if log_line.strip() and log_line != last_log_line:
                    # Save the last log line
                    last_log_line = log_line

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
