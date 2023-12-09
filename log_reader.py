import subprocess
import os

def monitor_logs(container_name, keywords):
    last_log_line = ""

    while True:
        # Get the last log line from the specified container
        command = f"docker logs --tail 1 {container_name}"
        try:
            output = subprocess.check_output(command, shell=True, text=True).strip()

            # Check if the log line has changed
            if output != last_log_line:
                # Save the last log line
                last_log_line = output

                # Check if any keyword is present in the log line
                if any(keyword in output for keyword in keywords):
                    # If a match is found, print the line to the console
                    print(output)

        except subprocess.CalledProcessError as e:
            print(f"Error while running 'docker logs': {e}")

        # No sleep, check logs continuously

if __name__ == "__main__":
    container_name = os.environ.get("MONITORED_CONTAINER", "bedrock_creative")
    keywords = os.environ.get("KEYWORDS", "").split(", ")

    monitor_logs(container_name, keywords)
