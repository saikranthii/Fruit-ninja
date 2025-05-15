import subprocess
import os
import sys
import time

def run_backend():
    return subprocess.Popen([sys.executable, "fruitninja.py"], cwd=os.getcwd())

def run_live_server():
    return subprocess.Popen([sys.executable, "-m", "http.server", "5500"], cwd=os.getcwd())

if __name__ == "__main__":
    backend_process = run_backend()
    time.sleep(2)  # Give backend time to start
    live_server_process = run_live_server()

    try:
        backend_process.wait()
    except KeyboardInterrupt:
        backend_process.terminate()
        live_server_process.terminate()