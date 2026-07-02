import subprocess
import time
import requests

def start_qdrant():
    result = subprocess.run(
        [
            "docker",
            "inspect",
            "-f",
            "{{.State.Running}}",
            "pdf-rag-qdrant"
        ],
        capture_output=True,
        text=True
    )

    # Container doesn't exist
    if result.returncode != 0:

        raise RuntimeError(
            "Qdrant container 'pdf-rag-qdrant' does not exist.\n"
            "Create it once using docker run."
        )

    # Container exists but stopped
    if result.stdout.strip() == "false":

        subprocess.run(
            [
                "docker",
                "start",
                "pdf-rag-qdrant"
            ]
        )

        print("✅ Qdrant started.")

    else:

        print("✅ Qdrant already running.")

def wait_for_backend():

    while True:

        try:

            response = requests.get(
                "http://127.0.0.1:8000/health",
                timeout=1
            )

            if response.status_code == 200:
                print("✅ FastAPI is ready.")
                return

        except requests.exceptions.RequestException:
            pass

        time.sleep(0.5)

if __name__ == "__main__":

    start_qdrant()

    backend = subprocess.Popen(
        [
            "uv",
            "run",
            "uvicorn",
            "src.backend.backend_api:app",
            "--reload"
        ]
    )

    wait_for_backend()

    frontend = subprocess.Popen(
        [
            "uv",
            "run",
            "streamlit",
            "run",
            "src/frontend/main.py"
        ]
    )

    time.sleep(3)
    print("✅ Application running successfully.")

    try:
        backend.wait()
        frontend.wait()

    except KeyboardInterrupt:

        print("\n🛑 Stopping application...")

        backend.terminate()
        frontend.terminate()

        backend.wait()
        frontend.wait()

        print("✅ Application stopped.")