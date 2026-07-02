# 📚 Smart PDF Reader - Session-Based RAG Chatbot

A modern **Retrieval-Augmented Generation (RAG)** application that enables users to interact with one or multiple PDF documents through natural language conversations.

The application combines **Streamlit**, **FastAPI**, **LangChain**, **Qdrant**, and **Groq LLMs** to provide an intelligent document assistant with persistent chat sessions and semantic retrieval.

---

# ✨ Features

## 📄 Document Processing

- Upload one or multiple PDF documents
- Automatic document chunking
- Semantic embeddings using HuggingFace
- Persistent vector storage with Qdrant
- Fast semantic retrieval using MMR Search

---

## 💬 Conversational AI

- Chat with uploaded PDFs
- Multi-turn conversations
- Context-aware responses
- Multiple Groq LLM support
- Source citations for every response

---

## 🗂 Session Management

- Automatic chat session creation
- Auto-generated session titles
- Continue previous conversations
- View complete chat history
- Delete chat sessions
- Session-specific vector collections

---

## 📊 Dashboard

- Uploaded PDF statistics
- Total document chunks
- Question count
- Recent sessions sidebar
- Uploaded document list

---

# 🏗 System Architecture

```text
                   Streamlit Frontend
                          │
                          │ HTTP
                          ▼
                   FastAPI Backend
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
        ▼                 ▼                 ▼
 Document Loader     Session Manager    RAG Pipeline
        │                 │                 │
        ▼                 ▼                 ▼
 Text Splitter      Chat History JSON   Groq LLM
        │
        ▼
 HuggingFace Embeddings
        │
        ▼
 Qdrant Vector Database
        │
        ▼
   MMR Retriever
        │
        ▼
 Generated Response
```

---

# ⚙️ Tech Stack

## Frontend

- Streamlit

## Backend

- FastAPI
- Python

## RAG Components

- LangChain
- HuggingFace Embeddings
- Qdrant Vector Database
- Groq LLM

## Document Processing

- PyPDFLoader
- RecursiveCharacterTextSplitter

## Storage

- Qdrant (Docker)
- JSON Session History

---

# 📁 Project Structure

```text
project/
│
├── src/
│   ├── backend/
│   │   ├── backend_api.py
│   │   ├── retriever.py
│   │   ├── rag_pipeline.py
│   │   ├── session_manager.py
│   │   └── doc_loader.py
│   │
│   └── frontend/
│       ├── main.py
│       ├── api.py
│       └── state.py
│
├── Chat_History/
├── run.py
├── pyproject.toml
├── uv.lock
└── README.md
```

---

# 🚀 Installation

## Clone Repository

```bash
git clone https://github.com/<your-username>/PDF_RAG_ChatBot.git

cd PDF_RAG_ChatBot
```

---

## Create Environment

```bash
uv venv

uv sync
```

---

## Configure Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=YOUR_GROQ_API_KEY
```

---

## Start Qdrant (First Time Only)

```bash
docker run -d ^
--name pdf-rag-qdrant ^
-p 6333:6333 ^
-v qdrant_storage:/qdrant/storage ^
qdrant/qdrant
```

---

# ▶ Running the Application

Simply execute:

```bash
uv run run.py
```

The launcher automatically:

- Starts the Qdrant container (if stopped)
- Starts the FastAPI backend
- Starts the Streamlit frontend

---

## Frontend

```
http://localhost:8501
```

## Backend

```
http://127.0.0.1:8000
```

---

# 🔄 Application Workflow

## 1. Upload Documents

Upload one or multiple PDF documents.

↓

## 2. Processing

- Load PDFs
- Split into chunks
- Generate embeddings
- Store vectors in Qdrant

↓

## 3. Session Creation

A new chat session is automatically created.

↓

## 4. Ask Questions

User queries are embedded and matched against relevant document chunks.

↓

## 5. Retrieval-Augmented Generation

Relevant context is combined with the user query and sent to the selected LLM.

↓

## 6. Session Persistence

The conversation, retrieved sources, and configuration are automatically saved for future use.

---

# 🤖 Supported Models

| UI Name | Groq Model |
|----------|------------|
| Llama | llama-3.1-8b-instant |
| GPT | llama-3.3-70b-versatile |

---

# 📌 Current Capabilities

- ✅ Multi-PDF Upload
- ✅ FastAPI REST Backend
- ✅ Session-Based Conversations
- ✅ Persistent Chat History
- ✅ Qdrant Vector Database
- ✅ Semantic Search
- ✅ Source Citations
- ✅ Continue Previous Sessions
- ✅ Delete Sessions
- ✅ Automatic Session Titles
- ✅ Docker Integration

---

# 🚀 Future Enhancements

- Rename Sessions
- Search Sessions
- Export Conversations
- Streaming Responses
- Hybrid Retrieval
- Contextual Compression Retriever
- Reranking Pipeline
- OCR for Scanned PDFs
- PDF Highlighting
- Multi-user Authentication

---

# 👨‍💻 Author

**Akshat Agarwal**

B.Tech Computer Science Engineering Student

Interested in:

- Retrieval-Augmented Generation (RAG)
- Large Language Models
- FastAPI
- LangChain
- Machine Learning
- Data Science

---

# 📜 License

This project is developed for educational purposes and portfolio demonstration.