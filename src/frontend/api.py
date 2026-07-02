import requests

BASE_URL = "http://127.0.0.1:8000"


# ---------------------------------------------------
# Upload PDFs
# ---------------------------------------------------

def upload_documents(files):

    return requests.post(
        f"{BASE_URL}/main/upload",
        files=files
    )


# ---------------------------------------------------
# Process PDFs
# ---------------------------------------------------

def process_documents(
    top_k,
    model,
    temperature,
    documents
):

    return requests.post(
        f"{BASE_URL}/main/process",
        json={
            "top_k": top_k,
            "model": model,
            "temperature": temperature,
            "documents": documents
        }
    )


# ---------------------------------------------------
# Chat
# ---------------------------------------------------

def chat(
    session_id,
    query,
    model_choice,
    temperature
):

    return requests.post(
        f"{BASE_URL}/main/chat",
        json={
            "session_id": session_id,
            "query": query,
            "model_choice": model_choice,
            "temp": temperature
        }
    )


# ---------------------------------------------------
# Health
# ---------------------------------------------------

def health():

    return requests.get(
        f"{BASE_URL}/health"
    )


# ---------------------------------------------------
# List Sessions
# ---------------------------------------------------

def list_sessions():

    return requests.get(
        f"{BASE_URL}/main/sessions"
    )


# ---------------------------------------------------
# Get Session
# ---------------------------------------------------

def get_session(session_id):

    return requests.get(
        f"{BASE_URL}/main/session/{session_id}"
    )

# ---------------------------------------------------
# Delete Session
# ---------------------------------------------------

def delete_session(session_id):

    return requests.delete(
        f"{BASE_URL}/main/session/{session_id}"
    )