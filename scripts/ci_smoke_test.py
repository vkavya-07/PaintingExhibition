"""CI smoke test: waits for the app to be available and checks /health and /paintings
Exits with non-zero code on failure so CI job fails.
"""
import sys
import time
import httpx

BASE = "http://127.0.0.1:8000"
TIMEOUT = 30


def wait_for(url: str, timeout: int = TIMEOUT):
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            r = httpx.get(url, timeout=5)
            if r.status_code == 200:
                return r
        except Exception:
            pass
        time.sleep(1)
    raise SystemExit(f"Timeout waiting for {url}")


def main():
    # health
    r = wait_for(f"{BASE}/health/")
    data = r.json()
    if data.get("status") != "ok":
        raise SystemExit("Health check returned unexpected payload")
    print("[smoke] /health OK")

    # paintings (should return 200 and a list)
    r = httpx.get(f"{BASE}/paintings/", headers={"x-role": "user"}, timeout=10)
    if r.status_code != 200:
        raise SystemExit(f"/paintings returned {r.status_code}")
    print("[smoke] /paintings OK")

    print("All smoke checks passed")


if __name__ == "__main__":
    main()
