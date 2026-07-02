
import streamlit as st 
import api 
from state import initialize_session_state, load_session_into_state

BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="ContextIQ - Smart PDF Reader",
    page_icon="📚",
    layout="wide"
)

# ---------------------------------------------------
# Session State
# ---------------------------------------------------
initialize_session_state()

def load_existing_session(session_id):

    response = api.get_session(session_id)

    if response.status_code != 200:

        st.error("Unable to load session.")

        return

    session = response.json()

    load_session_into_state(session)


# ---------------- HEADER ----------------
st.markdown("""
# 🧠 ContextIQ
> Chat with multiple PDFs using Retrieval-Augmented Document Intelligence Platform (RAG)
""")

# ---------------- SIDEBAR ----------------
with st.sidebar:

    st.title("⚙ Configuration")

    st.markdown("---")

    st.subheader("LLM Configuration")

    model = st.selectbox(
        "Model",
        [
            "GPT",
            "Llama"
        ]
    )

    temperature = st.slider(
        "Temperature",
        0.0,
        1.0,
        0.2,
        0.1
    )

    top_k = st.slider(
        "Top-K Retrieval",
        1,
        10,
        5
    )


    st.markdown("---")

    uploaded_files = st.file_uploader(
        "Upload PDF Documents",
        type=["pdf"],
        accept_multiple_files=True
    )

    if uploaded_files:

        st.success(
            f"{len(uploaded_files)} PDF(s) selected"
        )

    if st.button(
        "🚀 Process PDFs",
        use_container_width=True
    ):

        if not uploaded_files:

            st.warning(
                "Please upload one or more PDFs."
            )

        else:

            files = []

            st.session_state.uploaded_pdf_names = []

            for file in uploaded_files:
                st.session_state.uploaded_pdf_names.append(file.name)

                files.append((
                        "files",
                        (
                            file.name,
                            file.getvalue(),
                            "application/pdf"
                        )
                ))

            progress = st.progress(0)

            progress.progress(30)

            upload_response = api.upload_documents(files)

            progress.progress(60)

            process_response = api.process_documents(
                top_k,
                model,
                temperature,
                st.session_state.uploaded_pdf_names
            )

            progress.progress(100)
            process_data = process_response.json()

            st.session_state.current_session = process_data["session_id"]
            st.session_state.total_chunks = process_data["chunks"]
            st.session_state.documents_uploaded = len(uploaded_files)
            st.session_state.processed = True
            
            st.success("Documents processed successfully!")

    st.markdown("---")

    # ======================================================
    # Document Statistics
    # ======================================================

    st.subheader("📊 Document Statistics")

    metric1, metric2 = st.columns(2)

    with metric1:

        st.metric(
            "PDFs",
            st.session_state.documents_uploaded
        )

    with metric2:

        st.metric(
            "Chunks",
            st.session_state.total_chunks
        )

    questions = len(
        [
            x
            for x in st.session_state.messages
            if x["role"] == "user"
        ]
    )

    st.metric(
        "Questions Asked",
        questions
    )

    st.divider()

    # ======================================================
    # Uploaded PDFs
    # ======================================================

    st.subheader("📚 Uploaded PDFs")

    if len(st.session_state.uploaded_pdf_names) == 0:

        st.info(
            "No documents uploaded."
        )

    else:

        for pdf in st.session_state.uploaded_pdf_names:

            st.success(f"📄 {pdf}")

    st.divider()

    # ======================================================
    # Recent Sessions
    # ======================================================

    st.subheader("🕒 Recent Sessions")
    response = api.list_sessions()

    if response.status_code == 200:
        sessions = response.json()
    else:
        sessions = []

    if len(sessions) == 0:
        st.info("Session history will appear here.")

    else:
        for session in sessions:
            if not session.get("session_id"):
                continue

            documents = len(session["documents"])
            messages = session["total_messages"]
            title = session["title"]

            subtitle = (
                f"{documents} PDF(s) • "
                f"{messages//2} Question(s)"
            )
            st.info(f"Session ID : {session['session_id']}")

            if st.button(
                f"📚 {title}",
                key=f"session_{session['session_id']}",
                use_container_width=True
            ):

                load_existing_session(
                    session["session_id"]
                )
                st.rerun()

            if (
                st.session_state.pending_delete
                != session["session_id"]
            ):

                if st.button(
                    "🗑",
                    key=f"delete_{session['session_id']}",
                    use_container_width=True
                ):

                    st.session_state.pending_delete = (
                        session["session_id"]
                    )

                    st.rerun()

            else:
                st.warning("Are you sure you want to delete this Session?")

            st.caption(subtitle)

            if (
                st.session_state.pending_delete
                == session["session_id"]
            ):

                yes_col, cancel_col = st.columns(2)

                with yes_col:

                    if st.button(
                        "✅ Yes",
                        key=f"yes_{session['session_id']}",
                        use_container_width=True
                    ):

                        response = api.delete_session(
                            session["session_id"]
                        )

                        if response.status_code == 200:

                            st.session_state.pending_delete = None

                            st.success(
                                "Session deleted."
                            )

                            st.rerun()

                        else:

                            st.error(
                                "Unable to delete session."
                            )

                with cancel_col:

                    if st.button(
                        "❌ Cancel",
                        key=f"cancel_{session['session_id']}",
                        use_container_width=True
                    ):

                        st.session_state.pending_delete = None

                        st.rerun()

# ---------------- MAIN LAYOUT ----------------

st.subheader("💬 Conversation")

# ---------------------------------------
# Scrollable Chat Area
# ---------------------------------------
if len(st.session_state.messages) == 0:

    st.info("""
### 👋 Welcome!

Upload one or more PDF documents and click **Process PDFs**.

You can ask:

- Summarize this PDF
- Explain Chapter 2
- Compare two PDFs
- Generate interview questions
- List important concepts
""")

for message in st.session_state.messages:
    with st.chat_message(
        message["role"]
    ):
        st.markdown(message["content"])

        if message["role"] == "assistant":
            sources = message.get("sources", [])

            if sources:
                with st.expander("📚 View Sources"):
                    for source in sources:
                        st.markdown(
                            f"**📄 File:** {source['file_name']}"
                        )

                        st.markdown(
                            f"**📖 Page:** {source['page']}"
                        )

                        st.write(source["content"])
                        st.divider()

# ---------------------------------------
# Chat Input (Always below chat area)
# ---------------------------------------

prompt = st.chat_input(
    "Ask anything about your uploaded PDFs..."
)

if prompt:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    st.rerun()

# ---------------------------------------
# Generate Assistant Response
# ---------------------------------------

if (
    len(st.session_state.messages) > 0
    and st.session_state.messages[-1]["role"] == "user"
):

    prompt = st.session_state.messages[-1]["content"]

    status = st.status(
        "Generating Answer...",
        expanded=True
    )

    status.write("🔍 Retrieving relevant chunks...")

    response = api.chat(
        st.session_state.current_session,
        prompt,
        model,
        temperature
    )

    status.spinner("🧠 Running LLM...")

    status.write("✅ Response Generated")

    status.update(
        label="Completed",
        state="complete"
    )

    if response.status_code == 200:

        data = response.json()

        llm_response = data["AI_response"]

        st.session_state.last_retrieved_chunks = (
            data["retrieved_chunks"]
        )

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": llm_response,
                "sources": data["retrieved_chunks"]
            }
        )

        st.rerun()

    else:

        st.error(response.text)

    