from langchain_core.documents.base import Document
from src.backend.doc_loader import DocumentLoader
from src.backend.retriever import Retriever

from src.backend.rag_pipeline import RagPipeline
from src.backend.session_manager import SessionManager


from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Annotated


app = FastAPI()

class IndexRequest(BaseModel):
    top_k: int
    model: str
    temperature: float
    documents: List[str]

class ChatRequest(BaseModel):
    session_id: str
    query: str
    model_choice: str = "Llama"
    temp: float = 0.3




saved_files: List[Document] = []
retriever = Retriever()
session_manager = SessionManager()

@app.get("/debug")
def debug():
    return {
        "upload_type": str(List[UploadFile])
    }

@app.post("/main/upload")
def upload_files(
    files: Annotated[List[UploadFile], File()]
):
    global saved_files

    loader = DocumentLoader()
    loader.save_document(files)
    saved_files = loader.load_document()

    return {
        "message": "Files uploaded successfully",
        "documents": len(saved_files)
    }


@app.post("/main/process")
def process_documents(req: IndexRequest):
    global retriever

    if not saved_files:
        raise HTTPException(
            status_code=404,
            detail={
                "error": "Upload documents first"
            }
        )
    
    
    session_id = session_manager.create_session(
        documents=req.documents,
        model=req.model,
        temperature=req.temperature,
        top_k=req.top_k
    )
    retriever_obj, len_chunk = retriever.load_retriever(saved_files, session_id, req.top_k)

    return {
        "message": "Indexing completed",
        "chunks": len_chunk,
        "session_id": session_id
    }


@app.post("/main/chat")
def chat_with_llm(req: ChatRequest):
    session = session_manager.load_session(req.session_id)
    top_k = session["config"]["top_k"]

    retriever_obj = retriever.load_existing_retriever(
        req.session_id,
        top_k
    )

    context, retrieved_chunks = retriever.retrieve_context(
        retriever_obj,
        req.query
    )
    pipeline = RagPipeline(req.model_choice,req.temp)
    llm_response = pipeline.start_rag_pipeline(req.query,context)

    saved_chunks_text = []


    for doc in retrieved_chunks:

        saved_chunks_text.append(
            {
                "file_name":
                    doc.metadata.get(
                        "original_filename",
                        doc.metadata["source"].split("\\")[-1]
                    ),

                "page":
                    doc.metadata.get(
                        "page_label",
                        "N/A"
                    ),

                "content":
                    doc.page_content
            }
        )

    session_manager.append_message(
        session_id=req.session_id,
        role="user",
        content=req.query
    )

    session_manager.append_message(
        session_id=req.session_id,
        role="assistant",
        content=llm_response,
        sources=saved_chunks_text
    )

    return JSONResponse(
        status_code=200,
        content={
            "AI_response" : llm_response,
            "retrieved_chunks": saved_chunks_text,
            "total_chunks" : len(retrieved_chunks)
        }
    )

@app.get("/health")
def health():
    return {
        "documents_loaded":
            len(saved_files),
        "status": "healthy"
    }

@app.get("/main/sessions")
def list_all_sessions():

    sessions = session_manager.list_sessions()

    return JSONResponse(
        status_code=200,
        content=sessions
    )

@app.get("/main/session/{session_id}")
def get_session(session_id: str):

    try:

        session = session_manager.load_session(session_id)
        return JSONResponse(
            status_code=200,
            content=session
        )

    except FileNotFoundError:
        raise HTTPException(
            status_code=404,
            detail={
                "error": "Session not found"
            }
        )
    

@app.delete("/main/session/{session_id}")
def delete_session(session_id: str):

    try:
        session_manager.delete_session(session_id)
        retriever.delete_collection(session_id)

        return JSONResponse(
            status_code=200,
            content={
                "message": "Session deleted successfully"
            }
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )