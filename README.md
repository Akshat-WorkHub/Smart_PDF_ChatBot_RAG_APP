# 📚 Smart PDF Reader Chatbot

An intelligent PDF Question Answering application powered by a **Retrieval-Augmented Generation (RAG)** pipeline. The application allows users to upload PDF documents and interact with them using natural language queries. Relevant information is retrieved from the uploaded documents and provided to a Large Language Model (LLM) to generate accurate, context-aware responses.

---

## 🚀 Features

* 📄 Upload and process multiple PDF documents
* 🔍 Semantic search using vector embeddings
* 🧠 Retrieval-Augmented Generation (RAG) pipeline
* 🤖 Multiple LLM support (Groq-hosted models)
* 💬 Interactive chat interface built with Streamlit
* 📊 Document statistics dashboard
* 🎨 Light and Dark theme support
* ⚡ Fast retrieval using Qdrant Vector Store
* 📚 Context-aware question answering

---

## 🏗️ System Architecture

```text
PDF Upload
     │
     ▼
Document Loader (PyPDFLoader)
     │
     ▼
Text Chunking
(RecursiveCharacterTextSplitter)
     │
     ▼
Embedding Generation
(HuggingFace Embeddings)
     │
     ▼
Qdrant Vector Store
     │
     ▼
Retriever (MMR Search)
     │
     ▼
Prompt Construction
     │
     ▼
Groq LLM
     │
     ▼
Generated Answer
```

---

## 🛠️ Tech Stack

### Frontend

* Streamlit

### Backend

* Python

### AI & RAG Components

* LangChain
* HuggingFace Embeddings
* Qdrant Vector Database
* Groq LLM

### Document Processing

* PyPDFLoader
* RecursiveCharacterTextSplitter

### Utilities

* Python Dotenv

---

## 📂 Project Structure

```text
Smart_PDF_ChatBot_RAG_APP/
│
├── backend.py
├── main.py
├── light_theme.css
├── dark_theme.css
├── requirements.txt
├── pyproject.toml
├── .env
└── README.md
```

---

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/<username>/Smart_PDF_ChatBot_RAG_APP.git
cd Smart_PDF_ChatBot_RAG_APP
```

### Create Virtual Environment

Using UV:

```bash
uv venv
uv sync
```

or

```bash
uv add -r requirements.txt
```

### Configure Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=your_api_key_here
```

---

## ▶️ Running the Application

```bash
uv run streamlit run main.py
```

The application will be available at:

```text
http://localhost:8501
```

---

## 📖 How It Works

### Step 1: Upload PDFs

Users upload one or more PDF files through the Streamlit interface.

### Step 2: Document Processing

The uploaded PDFs are:

* Loaded using PyPDFLoader
* Split into smaller chunks
* Converted into vector embeddings

### Step 3: Vector Storage

Embeddings are stored in an in-memory Qdrant vector database.

### Step 4: Retrieval

When a user asks a question:

* The query is embedded
* Similar document chunks are retrieved using semantic search

### Step 5: Generation

Retrieved context and the user's query are provided to the selected LLM, which generates a context-aware response.

---

## 🤖 Supported Models

| UI Selection | Model Used              |
| ------------ | ----------------------- |
| Llama        | llama-3.1-8b-instant    |
| Mistral      | mixtral-8x7b-32768      |
| GPT          | llama-3.1-70b-versatile |
| Gemini       | gemma2-9b-it            |

---

## 📸 Future Enhancements

* Source citations with page numbers
* Persistent Qdrant storage
* Conversational memory
* Streaming responses
* PDF highlighting
* Multi-document comparison
* OCR support for scanned PDFs
* Export chat history

---

## 👨‍💻 Author

**Akshat Agarwal**

Computer Science Engineering Student | Data Science Enthusiast

---

## 📜 License

This project is intended for educational and learning purposes.
