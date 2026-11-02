# -*- coding: utf-8 -*-
"""
generation.py - Generate answers using ChatGroq with retrieved context
"""

import sys
from pathlib import Path
from typing import Any, Dict, List

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

load_dotenv(PROJECT_ROOT / ".env")

from exception.custom_exception import DocumentPortalException
from logger.custom_logger import CustomLogger
from src.retriever import ChromaRetriever

logger = CustomLogger().get_logger(__name__)


class RAGGenerator:
    """Generate answers using ChatGroq with retrieved context."""

    def __init__(
        self,
        chroma_persist_dir: str,
        collection_name: str = "pdf_documents",
        groq_model: str = "openai/gpt-oss-20b",
        groq_temperature: float = 0.0,
    ):
        try:
            self.retriever = ChromaRetriever(
                chroma_persist_dir=chroma_persist_dir,
                collection_name=collection_name,
            )
            
            self.llm = ChatGroq(
                model=groq_model,
                temperature=groq_temperature,
            )
            
            self.system_prompt = """You are an intelligent assistant that answers questions based on provided documents.
Answer based only on the context provided. If the answer is not in the context, say "I don't have information about that in the documents.\""""
            
            logger.info("rag_generator_initialized", model=groq_model)
        except Exception as exc:
            logger.exception("rag_generator_init_failed", error=str(exc))
            raise DocumentPortalException("Failed to initialize RAG generator", exc) from exc

    def generate_answer(self, query: str, k: int = 4) -> Dict[str, Any]:
        """Generate answer for query using retrieved context."""
        try:
            logger.info("generating_answer", query=query[:100])
            
            # Retrieve relevant documents
            retrieved_docs = self.retriever.retrieve(query, k=k)
            
            # Format context
            context_text = "\n\n".join([
                f"Document {i+1}:\n{doc.page_content}"
                for i, doc in enumerate(retrieved_docs)
            ])
            
            # Create prompt
            prompt_template = ChatPromptTemplate.from_messages([
                ("system", self.system_prompt),
                ("human", f"Context:\n{context_text}\n\nQuestion: {query}")
            ])
            
            # Generate answer
            messages = prompt_template.format_messages()
            response = self.llm.invoke(messages)
            
            logger.info("answer_generated", query_length=len(query))
            
            return {
                "answer": response.content,
                "retrieved_docs": retrieved_docs,
                "doc_count": len(retrieved_docs),
            }
        except Exception as exc:
            logger.exception("answer_generation_failed", error=str(exc))
            raise DocumentPortalException("Failed to generate answer", exc) from exc
