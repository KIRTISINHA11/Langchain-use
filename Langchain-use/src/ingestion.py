# -*- coding: utf-8 -*-
"""
ingestion.py - Document ingestion pipeline for RAG
Converts parsed PDF documents into vector embeddings and stores in Chroma.
"""

import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_groq import ChatGroq
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException

logger = CustomLogger().get_logger(__name__)


class DocumentIngestionPipeline:
    """Ingest parsed PDF documents into Chroma vector database."""

    def __init__(
        self,
        chroma_persist_dir: str,
        embedding_model: str = "all-MiniLM-L6-v2",
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
        groq_model: str = "openai/gpt-oss-20b",
        groq_temperature: float = 0.0,
    ):
        self.chroma_persist_dir = Path(chroma_persist_dir)
        self.embedding_model_name = embedding_model
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.groq_model = groq_model
        self.groq_temperature = groq_temperature
        self.embeddings = None
        self.vector_store = None
        self.llm = None
        self.retriever = None

        try:
            self._create_chroma_directory()
            self._initialize_embeddings()
            self._initialize_llm()
            logger.info("ingestion_pipeline_initialized", chroma_dir=str(self.chroma_persist_dir))
        except Exception as exc:
            logger.exception("ingestion_pipeline_initialization_failed", error=str(exc))
            raise DocumentPortalException("Failed to initialize ingestion pipeline", exc) from exc

    def _create_chroma_directory(self) -> None:
        try:
            self.chroma_persist_dir.mkdir(parents=True, exist_ok=True)
            logger.debug("chroma_directory_created", directory=str(self.chroma_persist_dir))
        except Exception as exc:
            logger.exception("chroma_directory_creation_failed", error=str(exc))
            raise DocumentPortalException("Failed to create Chroma directory", exc) from exc

    def _initialize_embeddings(self) -> None:
        try:
            logger.info("initializing_embeddings", model=self.embedding_model_name)
            self.embeddings = HuggingFaceEmbeddings(model_name=self.embedding_model_name)
            logger.info("embeddings_initialized_successfully", model=self.embedding_model_name)
        except Exception as exc:
            logger.exception("embeddings_initialization_failed", error=str(exc))
            raise DocumentPortalException("Failed to initialize embeddings", exc) from exc

    def _initialize_llm(self) -> None:
        try:
            logger.info("initializing_groq_llm", model=self.groq_model)
            self.llm = ChatGroq(model=self.groq_model, temperature=self.groq_temperature)
            logger.info("groq_llm_initialized_successfully", model=self.groq_model)
        except Exception as exc:
            logger.exception("groq_llm_initialization_failed", error=str(exc))
            raise DocumentPortalException("Failed to initialize ChatGroq LLM", exc) from exc

    def _split_documents(self, documents: List[Document]) -> List[Document]:
        try:
            logger.info("splitting_documents", total_documents=len(documents), chunk_size=self.chunk_size)
            splitter = RecursiveCharacterTextSplitter(
                chunk_size=self.chunk_size,
                chunk_overlap=self.chunk_overlap,
                separators=["\n\n", "\n", ".", " ", ""],
            )
            split_docs = splitter.split_documents(documents)
            logger.info("documents_split_successfully", split_count=len(split_docs))
            return split_docs
        except Exception as exc:
            logger.exception("document_splitting_failed", error=str(exc))
            raise DocumentPortalException("Failed to split documents", exc) from exc

    def ingest_documents(
        self,
        documents: List[Document],
        collection_name: str = "pdf_documents",
        split_documents: bool = True,
    ) -> Chroma:
        try:
            logger.info("document_ingestion_started", total_documents=len(documents), collection_name=collection_name)
            if split_documents:
                docs_to_ingest = self._split_documents(documents)
            else:
                docs_to_ingest = documents
            logger.info("creating_chroma_vector_store", collection_name=collection_name)
            self.vector_store = Chroma.from_documents(
                documents=docs_to_ingest,
                embedding=self.embeddings,
                collection_name=collection_name,
                persist_directory=str(self.chroma_persist_dir),
            )
            self.retriever = self.vector_store.as_retriever(search_kwargs={"k": 4})
            logger.info("document_ingestion_completed_successfully", documents_ingested=len(docs_to_ingest))
            return self.vector_store
        except Exception as exc:
            logger.exception("document_ingestion_failed", error=str(exc))
            raise DocumentPortalException("Failed to ingest documents into Chroma", exc) from exc

    def similarity_search(self, query: str, k: int = 4) -> List[Document]:
        if not self.vector_store:
            raise DocumentPortalException("Vector store not initialized. Call ingest_documents() first.", None)
        try:
            logger.info("similarity_search_started", query=query[:100], k=k)
            results = self.vector_store.similarity_search(query, k=k)
            logger.info("similarity_search_completed", results_found=len(results))
            return results
        except Exception as exc:
            logger.exception("similarity_search_failed", error=str(exc))
            raise DocumentPortalException("Failed to perform similarity search", exc) from exc

    def similarity_search_with_score(self, query: str, k: int = 4) -> List[tuple]:
        if not self.vector_store:
            raise DocumentPortalException("Vector store not initialized. Call ingest_documents() first.", None)
        try:
            logger.info("similarity_search_with_score_started", query=query[:100], k=k)
            results = self.vector_store.similarity_search_with_score(query, k=k)
            logger.info("similarity_search_with_score_completed", results_found=len(results))
            return results
        except Exception as exc:
            logger.exception("similarity_search_with_score_failed", error=str(exc))
            raise DocumentPortalException("Failed to perform similarity search with score", exc) from exc

    def get_retriever(self, search_kwargs: Optional[Dict[str, Any]] = None):
        if not self.vector_store:
            raise DocumentPortalException("Vector store not initialized. Call ingest_documents() first.", None)
        try:
            if search_kwargs is None:
                search_kwargs = {"k": 4}
            logger.info("creating_retriever", search_kwargs=search_kwargs)
            retriever = self.vector_store.as_retriever(search_kwargs=search_kwargs)
            logger.info("retriever_created_successfully")
            return retriever
        except Exception as exc:
            logger.exception("retriever_creation_failed", error=str(exc))
            raise DocumentPortalException("Failed to create retriever", exc) from exc

    def get_llm(self) -> ChatGroq:
        if not self.llm:
            raise DocumentPortalException("LLM not initialized.", None)
        return self.llm

    def get_embeddings(self) -> HuggingFaceEmbeddings:
        if not self.embeddings:
            raise DocumentPortalException("Embeddings not initialized.", None)
        return self.embeddings

    def get_collection_stats(self) -> Dict[str, Any]:
        try:
            if not self.vector_store:
                raise DocumentPortalException("Vector store not initialized.", None)
            collection = self.vector_store._collection
            count = collection.count()
            stats = {
                "collection_name": collection.name,
                "document_count": count,
                "embedding_model": self.embedding_model_name,
                "persist_directory": str(self.chroma_persist_dir),
            }
            logger.info("collection_stats_retrieved")
            return stats
        except Exception as exc:
            logger.exception("collection_stats_retrieval_failed", error=str(exc))
            raise DocumentPortalException("Failed to retrieve collection statistics", exc) from exc
