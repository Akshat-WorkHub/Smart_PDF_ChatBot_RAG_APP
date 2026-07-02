from langchain_groq import ChatGroq # LLM 
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
load_dotenv()

from src.backend.doc_loader import DocumentLoader
from src.backend.retriever import Retriever
from src.backend.prompt import SystemPrompt

import os
import tempfile
import streamlit as st

class RagPipeline:
    def __init__(self, model_choice, temperature):
        self.prompt = SystemPrompt
        self.llm_model = self.load_llm_model(model_choice,temperature)
        self.parser = StrOutputParser()

    def load_llm_model(self, model_choice: str, temperature: float):
        """
            Maps your Streamlit dropdown string choices directly to actual Groq LLM instances.
        """
        models_list = {
            "Llama": "llama-3.3-70b-versatile",
            "GPT": "openai/gpt-oss-20b" 
        }
        selected_model = models_list.get(model_choice, "llama-3.1-8b-instant")
        
        return ChatGroq(
            model=selected_model,
            temperature=temperature # Injected dynamically from st.slider
        )

    def start_rag_pipeline(self, query, context):
        try:
            
            chain = self.prompt | self.llm_model | self.parser
            response = chain.invoke({
                "query" : query,
                "context" : context
            })

            return response
        except Exception as e:
            return f"Error: {str(e)}"