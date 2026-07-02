from langchain_core.prompts import PromptTemplate # For defining SystemPrompt Template

SystemPrompt = PromptTemplate(
    template="""
You are a helpful AI assistant.

Answer the user's question ONLY using the provided context.

User Query:
{query}

Retrieved Context:
{context}

Instructions:
1. If the answer can be inferred from the retrieved context, answer clearly.
2. If the query asks for a summary, summarize ONLY the retrieved context.
3. If the context contains no information relevant to the query, reply:
   "Don't have Relevant information about your query."
4. Do not make up information not present in the context.
""",
    input_variables=["query", "context"]
)