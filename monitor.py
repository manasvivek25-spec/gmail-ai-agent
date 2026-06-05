import time
import subprocess
import sys

while True:

    print("Checking emails...")

    subprocess.run([
        sys.executable,
        "main.py"
    ])

    print("Sleeping for 10 seconds...")

    time.sleep(10)