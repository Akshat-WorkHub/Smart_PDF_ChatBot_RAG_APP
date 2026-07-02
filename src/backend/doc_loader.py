from langchain_community.document_loaders import PyPDFLoader # PDF Document Loader
import os
import tempfile

class DocumentLoader:
    def __init__(self):
        self.all_documents = []

    def save_document(self, uploaded_files):

        # Loop through the Streamlit uploaded file streams
        for uploaded_file in uploaded_files:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
                temp_file.write(uploaded_file.file.read())
                temp_path = temp_file.name
                
            try:
                loader = PyPDFLoader(temp_path)
                documents = loader.load()
                for doc in documents:
                    doc.metadata["original_filename"] = uploaded_file.filename
                self.all_documents.extend(documents)

            finally:
                # 4. Clean up and delete the temporary file from disk to save space
                if os.path.exists(temp_path):
                    os.remove(temp_path)
       

    def load_document(self):
        return self.all_documents


