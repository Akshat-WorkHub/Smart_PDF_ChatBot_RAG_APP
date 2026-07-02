from langchain_text_splitters import RecursiveCharacterTextSplitter # Text Splitter
from langchain_huggingface import HuggingFaceEmbeddings # Embedding Model
from langchain_qdrant import QdrantVectorStore # Vector DB to store Embeddings
from qdrant_client import QdrantClient
from src.frontend import api

class Retriever:

    def load_embedding_model(self):
        return HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

    def build_vector_store(self, docs, session_id):

        embedding_model = self.load_embedding_model()

        vector_store = QdrantVectorStore.from_documents(
            documents=docs,
            embedding=embedding_model,
            url="http://localhost:6333",
            collection_name=session_id
        )

        return vector_store
    
    

    def load_retriever(self, documents, session_id, top_k):
        splitter = RecursiveCharacterTextSplitter(chunk_size=300)
        docs = splitter.split_documents(documents)

        vector_store = self.build_vector_store(docs, session_id)
        retriever = vector_store.as_retriever(
            search_type="mmr", 
            search_kwargs={"k" : top_k}
        )
        return retriever, len(docs)
    
    def load_existing_retriever(self, session_id, top_k):

        embedding_model = self.load_embedding_model()
        
        client = QdrantClient(
            url="http://localhost:6333"
        )

        vector_store = QdrantVectorStore(
            client=client,
            collection_name=session_id,
            embedding=embedding_model
        )

        retriever = vector_store.as_retriever(
            search_type="mmr",
            search_kwargs={"k": top_k}
        )


        response = api.get_session(session_id)
        print("Printing Existing retriever response")
        print(response.json())
        return retriever
    
    def retrieve_context(self, retriever, query):
        retrieved_chunks = retriever.invoke(query)

        context = "\n\n".join([chunk.page_content for chunk in retrieved_chunks])
        return context, retrieved_chunks
    
    def delete_collection(self, session_id ):
        client = QdrantClient(url="http://localhost:6333")
        if client.collection_exists(collection_name=session_id):
            client.delete_collection(collection_name=session_id)


    