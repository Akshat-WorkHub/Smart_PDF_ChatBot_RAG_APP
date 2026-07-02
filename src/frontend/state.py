import streamlit as st

DEFAULTS = {
    "current_session": None,
    "chat_sessions": [],
    "total_chunks": 0,
    "last_retrieved_chunks": [],
    "uploaded_pdf_names": [],
    "documents_uploaded": 0,
    "messages": [],
    "pending_delete": None,
    "processed": False
}


def initialize_session_state():

    for key, value in DEFAULTS.items():
        if key not in st.session_state:
            st.session_state[key] = value

def load_session_into_state(session):
    st.session_state.current_session = (
        session["session_id"]
    )

    st.session_state.messages = (
        session["messages"]
    )

    st.session_state.uploaded_pdf_names = (
        session["documents"]
    )

    st.session_state.documents_uploaded = (
        len(session["documents"])
    )

    st.session_state.processed = True