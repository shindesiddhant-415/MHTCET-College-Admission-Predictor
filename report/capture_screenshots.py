"""
Script to capture high-resolution screenshots of all deployed React application tabs
using headless Chrome and the local FastAPI + React production server.
"""

import os
import sys

# Ensure project root is in Python sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import time
import subprocess
import threading
import urllib.request

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
OUTPUT_DIR = r"D:\AIML-PROJECT\report\screenshots"
os.makedirs(OUTPUT_DIR, exist_ok=True)

TABS = [
    ("overview", "app_overview_tab.png"),
    ("recommend", "app_recommendations_tab.png"),
    ("trends", "app_trends_tab.png"),
    ("performance", "app_model_performance_tab.png"),
    ("compare", "app_comparison_tab.png"),
    ("dataset", "app_dataset_tab.png")
]

def wait_for_server(url="http://127.0.0.1:8000/api/health", timeout=20):
    start = time.time()
    while time.time() - start < timeout:
        try:
            with urllib.request.urlopen(url, timeout=1) as resp:
                if resp.status == 200:
                    return True
        except Exception:
            time.sleep(0.5)
    return False

def capture_tab(tab_id, out_name):
    url = f"http://127.0.0.1:8000/?tab={tab_id}"
    out_path = os.path.join(OUTPUT_DIR, out_name)
    print(f"Capturing tab '{tab_id}' -> {out_name} ...")
    cmd = [
        CHROME_PATH,
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--window-size=1440,900",
        "--virtual-time-budget=7000",
        f"--screenshot={out_path}",
        url
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if os.path.exists(out_path):
        size = os.path.getsize(out_path)
        print(f"  [OK] Saved {out_name} ({size:,} bytes)")
    else:
        print(f"  [FAIL] Could not capture {out_name}: {res.stderr}")

def main():
    print("Starting FastAPI backend process via subprocess.Popen...")
    env = os.environ.copy()
    env["PYTHONPATH"] = BASE_DIR
    proc = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "api.main:app", "--host", "127.0.0.1", "--port", "8000"],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    try:
        if not wait_for_server():
            print("Error: FastAPI server failed to start within timeout.")
            stdout, stderr = proc.communicate(timeout=2)
            print("Server stdout:", stdout.decode("utf-8", errors="ignore"))
            print("Server stderr:", stderr.decode("utf-8", errors="ignore"))
            sys.exit(1)
        print("FastAPI server active and healthy on port 8000.")

        for tab_id, out_name in TABS:
            capture_tab(tab_id, out_name)

        print("\nAll application tab screenshots captured successfully!")
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=3)
        except Exception:
            proc.kill()

if __name__ == "__main__":
    main()
