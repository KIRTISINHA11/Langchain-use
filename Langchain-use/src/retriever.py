# -*- coding: utf-8 -*-
"""
retriever.py - Retrieve documents from Chroma vector store
"""

import sys
from pathlib import Path
from typing import Any, List

from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

load_dotenv(PROJECT_ROOT / ".env")

from exception.custom_exception import DocumentPortalException
from logger.custom_logger import CustomLogger

logger = CustomLogger().get_logger(__name__)


class ChromaRetriever:
    """Retrieve documents from Chroma vector store."""

    def __init__(
        self,
        chroma_persist_dir: str,
        collection_name: str = "pdf_documents",
        embedding_model: str = "all-MiniLM-L6-v2",
    ):
        try:
            self.chroma_persist_dir = Path(chroma_persist_dir)
            self.collection_name = collection_name
            self.embeddings = HuggingFaceEmbeddings(model_name=embedding_model)
            
            self.vector_store = Chroma(
                collection_name=collection_name,
                embedding_function=self.embeddings,
                persist_directory=str(self.chroma_persist_dir),
            )
            
            logger.info("chroma_retriever_initialized", collection=collection_name)
        except Exception as exc:
            logger.exception("chroma_retriever_init_failed", error=str(exc))
            raise DocumentPortalException("Failed to initialize Chroma retriever", exc) from exc

    def retrieve(self, query: str, k: int = 4) -> List[Document]:
        """Retrieve top-k documents for query."""
        try:
            logger.info("retrieving_documents", query=query[:100], k=k)
            results = self.vector_store.similarity_search(query, k=k)
            logger.info("documents_retrieved", count=len(results))
            return results
        except Exception as exc:
            logger.exception("retrieval_failed", error=str(exc))
            raise DocumentPortalException("Failed to retrieve documents", exc) from exc

    def retrieve_with_scores(self, query: str, k: int = 4) -> List[tuple]:
        """Retrieve with relevance scores."""
        try:
            results = self.vector_store.similarity_search_with_score(query, k=k)
            return results
        except Exception as exc:
            logger.exception("retrieval_with_scores_failed", error=str(exc))
            raise DocumentPortalException("Failed to retrieve with scores", exc) from exc
