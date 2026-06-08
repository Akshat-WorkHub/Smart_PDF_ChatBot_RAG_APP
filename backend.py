from langchain_community.document_loaders import PyPDFLoader # PDF Document Loader
from langchain_text_splitters import RecursiveCharacterTextSplitter # Text Splitter
from langchain_huggingface import HuggingFaceEmbeddings # Embedding Model
from langchain_qdrant import QdrantVectorStore # Vector DB to store Embeddings

from langchain_core.prompts import PromptTemplate # For defining SystemPrompt Template

from langchain_groq import ChatGroq # LLM 

from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
load_dotenv()

import os
import tempfile
import streamlit as st

@st.cache_resource
def load_embedding_model():
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

@st.cache_resource
def build_vector_store(docs):

    embedding_model = load_embedding_model()

    vector_store = QdrantVectorStore.from_documents(
        documents=docs,
        embedding=embedding_model,
        location=":memory:",
        collection_name="pdf_chat_history"
    )

    return vector_store

def get_retriever(uploaded_files, top_k):

    all_documents = []

    # Loop through the Streamlit uploaded file streams
    for uploaded_file in uploaded_files:
        
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            
            temp_file.write(uploaded_file.getbuffer())
            temp_path = temp_file.name
            
        try:
            
            loader = PyPDFLoader(temp_path)
            documents = loader.load()
            all_documents.extend(documents)
        finally:
            # 4. Clean up and delete the temporary file from disk to save space
            if os.path.exists(temp_path):
                os.remove(temp_path)


    splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
    )
    docs = splitter.split_documents(all_documents)
    vector_store = build_vector_store(docs)

    retriever = vector_store.as_retriever(search_type="mmr", search_kwargs={"k" : top_k})
    return retriever, len(docs)

def start_retriever(query, retriever_model):
    retrieved_chunks = retriever_model.invoke(query)

    context = "\n\n".join([chunk.page_content for chunk in retrieved_chunks])
    return context, retrieved_chunks



def get_llm_model(ui_model_choice: str, temperature: float):
    """
    Maps your Streamlit dropdown string choices directly to actual Groq LLM instances.
    """
    model_mapping = {
        "Llama": "llama-3.1-8b-instant",
        "Mistral": "mixtral-8x7b-32768",
        "Gemini": "gemma2-9b-it", 
        "GPT": "llama-3.1-70b-versatile" 
    }
    
    # Fallback to Llama if something weird happens
    selected_model_string = model_mapping.get(ui_model_choice, "llama-3.1-8b-instant")
    
    return ChatGroq(
        model=selected_model_string,
        temperature=temperature # Injected dynamically from st.slider
    )

def start_rag_pipeline(ques, model, retriever):
    try:
        print("RAG PIPELINE RUNNING")
        
        SystemPrompt = PromptTemplate(
            template="""
            You are helpful AI Assistant and your goal is to answer the relevant query of user from given retrieved context only.
            Here are given User Query & Context Retrieved
            User Query : {query}
            Context : {context}

            Note : If user query is out of syllabus from given Context Just Say "Don't have Relevant information about your query" and paste user query after this line.
            """,
            input_variables=["query","context"]
        )
        
        parser = StrOutputParser()
        chain = SystemPrompt | model | parser
        context, chunks = start_retriever(ques, retriever)
        result = chain.invoke({
            "query" : ques,
            "context" : context
        })

        return result, chunks
    except Exception as e:
        return f"Error: {str(e)}"
