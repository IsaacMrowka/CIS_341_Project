import subprocess
import time

# Keep the program running
while True:

    print("Starting audit scan...", flush=True)

    # Run the monitoring program
    result = subprocess.run(["python3", "system_security_daemon.py"])

    # Stop if the program fails
    if result.returncode != 0:
        print("Audit scan failed.", flush=True)
        break

    # Wait 60 seconds before running again
    print("Waiting 60 seconds...", flush=True)
    time.sleep(60)