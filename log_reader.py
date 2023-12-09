import subprocess
import os

def monitor_logs(container_name, keywords):
    # Use the --follow option to continuously tail the logs
    command = f"docker logs --follow {container_name}"
    
    # Use subprocess.Popen to get continuous output from the command
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, text=True)

    try:
        # Read the output line by line
        for line in process.stdout:
            # Check if any keyword is present in the log line
            if any(keyword in line for keyword in keywords):
                # Replace "INFO]" with "TRUE]" if a keyword is found
                line = line.replace("INFO]", "TRUE]")
                # Print the modified line to the console
                print(line, end='', flush=True)

    except KeyboardInterrupt:
        # Handle KeyboardInterrupt to gracefully stop the script
        pass
    finally:
        # Close the subprocess when done
        process.kill()

if __name__ == "__main__":
    container_name = os.environ.get("MONITORED_CONTAINER", "bedrock_creative")
    keywords = os.environ.get("KEYWORDS", "").split(", ")

    monitor_logs(container_name, keywords)
