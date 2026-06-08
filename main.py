import streamlit as st
from backend import (
    get_retriever,
    get_llm_model,
    start_rag_pipeline
)

import time
start = time.time()

print("APP RERUN")
# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Smart PDF Reader",
    page_icon="📚",
    layout="wide"
)
if "messages" not in st.session_state:
    st.session_state.messages = []

if "retriever" not in st.session_state:
    st.session_state.retriever = None

if "total_chunks" not in st.session_state:
    st.session_state.total_chunks = 0

if "theme" not in st.session_state:
    st.session_state.theme = "Light"

# ---------------- CUSTOM CSS ----------------
css_file = (
    "dark_theme.css"
    if st.session_state.theme == "Dark"
    else "light_theme.css"
)

with open(css_file) as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )

# ---------------- HEADER ----------------
st.markdown(
    "<div class='title'>📚 Smart PDF Reader Chatbot</div>",
    unsafe_allow_html=True
)
st.markdown(
    "<div class='subtitle'>Upload PDFs | Ask Questions | Retrieve Context using RAG</div>",
    unsafe_allow_html=True
)

# ---------------- SIDEBAR ----------------
with st.sidebar:

    st.header("⚙️ Configuration")

    theme_toggle = st.toggle(
        "🌙 Dark Mode",
        value=(st.session_state.theme == "Dark")
    )

    st.session_state.theme = (
        "Dark"
        if theme_toggle
        else "Light"
    )

    uploaded_files = st.file_uploader(
        "Upload PDF Files",
        type=["pdf"],
        accept_multiple_files=True 
    )

    st.divider()
    
    model = st.selectbox( "LLM Model",["Gemini","GPT","Llama","Mistral"])
    temperature = st.slider("Temperature",0.0,1.0,0.2)
    top_k = st.slider("Top K Chunks",1,10,5)
    

    st.divider()

    if st.button("Process PDFs", use_container_width=True):
        print("PROCESS PDF CLICKED")
        if uploaded_files:
            with st.spinner("Processing PDFs..."):

                retriever, total_chunks = get_retriever(
                    uploaded_files=uploaded_files,
                    top_k=top_k
                )

                st.session_state.retriever = retriever
                st.session_state.total_chunks = total_chunks

            st.success("PDFs Processed Successfully")

        else:
            st.warning("Please upload at least one PDF")
    
    st.sidebar.write(
        f"Render Time: {round(time.time() - start, 2)} sec"
    )

# ---------------- MAIN LAYOUT ----------------
col1, col2 = st.columns([3, 1])
with col1:

    st.subheader("💬 Chat Assistant")

    # Display previous chat
    for message in st.session_state.messages:

        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    prompt = st.chat_input(
        "Ask something about your uploaded PDF..."
    )

    if prompt:
        st.session_state.messages.append(
            {
                "role": "user",
                "content": prompt
            }
        )

        with st.chat_message("user"):
            st.markdown(prompt)

        if st.session_state.retriever is None:

            st.error("Please upload and process PDFs first.")

        else:

            dynamic_llm = get_llm_model(
                ui_model_choice=model,
                temperature=temperature
            )

            with st.spinner("Thinking..."):
                response_text, chunks = start_rag_pipeline(
                    ques=prompt,
                    model=dynamic_llm,
                    retriever=st.session_state.retriever
                )

                st.session_state.last_retrieved_chunks = chunks

            with st.chat_message("assistant"):
                st.markdown(response_text)

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": response_text
                }
            )

with col2:

    st.subheader("📄 Document Stats")

    st.metric("PDFs Uploaded", len(uploaded_files) if uploaded_files else 0)

    st.metric(
        "Chunks Indexed",
        st.session_state.total_chunks
    )

    st.metric("Questions Asked", len(
        [m for m in st.session_state.messages if m["role"] == "user"]
    ))

    st.divider()

    st.subheader("🔍 Retrieved Context")

    st.info(
        """
        Retrieved chunks from vector database
        will appear here after each query.
        """
    )

    st.divider()

    st.subheader("📜 Chat History")

    for idx, msg in enumerate(
            [m for m in st.session_state.messages if m["role"] == "user"],
            start=1):
        st.write(f"{idx}. {msg['content'][:40]}...")