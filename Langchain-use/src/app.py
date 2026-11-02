# -*- coding: utf-8 -*-
"""
app.py

Complete RAG Application using LangChain.
Integrates PDF parsing, document ingestion, and retrieval-generation pipeline.
"""

import sys
from pathlib import Path
from typing import Optional

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document

from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException
from data_parsing import MultimodalPDFParser
from ingestion import DocumentIngestionPipeline

logger = CustomLogger().get_logger(__name__)


class RAGApplication:
    """
    Complete Retrieval-Augmented Generation (RAG) Application.
    
    Pipeline:
    1. Parse PDF → Extract text, images, tables
    2. Ingest documents → Create vector embeddings with Chroma
    3. Build RAG chain → Retrieval + LLM generation
    4. Answer queries → Retrieve context + generate responses
    """

    def __init__(
        self,
        pdf_path: str,
        data_dir: str,
        chroma_dir: str,
    ):
        """
        Initialize RAG application.
        
        Args:
            pdf_path: Path to PDF file
            data_dir: Directory for parsed outputs
            chroma_dir: Directory for Chroma vector database
        """
        self.pdf_path = pdf_path
        self.data_dir = Path(data_dir)
        self.chroma_dir = Path(chroma_dir)
        
        self.parser = None
        self.pipeline = None
        self.retriever = None
        self.rag_chain = None
        
        logger.info(
            "rag_application_initialized",
            pdf_path=pdf_path,
            data_dir=str(self.data_dir),
            chroma_dir=str(self.chroma_dir),
        )

    def setup(self) -> None:
        """Setup complete RAG pipeline."""
        try:
            logger.info("rag_setup_started")
            
            # Step 1: Initialize parser
            logger.info("step_1_initializing_parser")
            self.parser = MultimodalPDFParser(
                pdf_path=self.pdf_path,
                output_dir=str(self.data_dir),
                render_scale=2.0,
            )
            
            # Step 2: Parse PDF
            logger.info("step_2_parsing_pdf")
            parse_result = self.parser.parse(save_output=True)
            documents = parse_result["documents"]
            logger.info("pdf_parsed", document_count=len(documents))
            
            # Step 3: Initialize ingestion pipeline
            logger.info("step_3_initializing_ingestion_pipeline")
            self.pipeline = DocumentIngestionPipeline(
                chroma_persist_dir=str(self.chroma_dir),
                embedding_model="all-MiniLM-L6-v2",
                chunk_size=1000,
                chunk_overlap=200,
                groq_model="openai/gpt-oss-20b",
                groq_temperature=0.0,
            )
            
            # Step 4: Ingest documents into Chroma
            logger.info("step_4_ingesting_documents")
            self.pipeline.ingest_documents(
                documents=documents,
                collection_name="pdf_documents",
                split_documents=True,
            )
            logger.info("documents_ingested")
            
            # Step 5: Create retriever
            logger.info("step_5_creating_retriever")
            self.retriever = self.pipeline.get_retriever({"k": 4})
            
            # Step 6: Build RAG chain
            logger.info("step_6_building_rag_chain")
            self._build_rag_chain()
            
            logger.info("rag_setup_completed_successfully")
            
        except Exception as exc:
            logger.exception("rag_setup_failed", error=str(exc))
            raise DocumentPortalException("Failed to setup RAG application", exc) from exc

    def _build_rag_chain(self) -> None:
        """Build LangChain RAG chain."""
        try:
            logger.info("building_rag_chain")
            
            # Define prompt template
            prompt_template = ChatPromptTemplate.from_template("""
You are an intelligent assistant that answers questions based on provided documents.

Context from documents:
{context}

Question: {input}

Answer based on the context provided. If the answer is not in the context, say "I don't have information about that in the documents."
""")
            
            # Get LLM
            llm = self.pipeline.get_llm()
            
            # Create document chain
            document_chain = create_stuff_documents_chain(llm, prompt_template)
            
            # Create RAG chain
            self.rag_chain = create_retrieval_chain(
                self.retriever,
                document_chain
            )
            
            logger.info("rag_chain_built_successfully")
            
        except Exception as exc:
            logger.exception("rag_chain_building_failed", error=str(exc))
            raise DocumentPortalException("Failed to build RAG chain", exc) from exc

    def query(self, question: str) -> dict:
        """
        Query the RAG system.
        
        Args:
            question: User question
            
        Returns:
            Dictionary with answer and source documents
        """
        if not self.rag_chain:
            raise DocumentPortalException(
                "RAG chain not initialized. Call setup() first.",
                None,
            )
        
        try:
            logger.info("query_started", question=question[:100])
            
            result = self.rag_chain.invoke({"input": question})
            
            logger.info(
                "query_completed",
                question=question[:100],
                answer_length=len(result.get("answer", "")),
            )
            
            return result
            
        except Exception as exc:
            logger.exception("query_failed", question=question[:100], error=str(exc))
            raise DocumentPortalException("Failed to process query", exc) from exc

    def get_collection_stats(self) -> dict:
        """Get vector database statistics."""
        try:
            if not self.pipeline:
                raise DocumentPortalException("Pipeline not initialized.", None)
            
            stats = self.pipeline.get_collection_stats()
            logger.info("collection_stats_retrieved")
            return stats
            
        except Exception as exc:
            logger.exception("collection_stats_failed", error=str(exc))
            raise DocumentPortalException("Failed to get collection stats", exc) from exc


def main():
    """Main entry point for RAG application."""
    logger.info("rag_application_started")
    
    try:
        # Configuration
        DATA_DIR = Path(r"C:\Users\Admin\Agentic AI Projects\AI\RAG\Langchain-use\data")
        PDF_PATH = DATA_DIR / "Client_Contracts_Policies_and_Incident_Records.pdf"
        PARSE_OUTPUT_DIR = DATA_DIR / "parsed_pdf_output"
        CHROMA_DIR = DATA_DIR / "chroma_vectorstore"
        
        print("\n" + "="*70)
        print("🤖 MULTIMODAL RAG APPLICATION")
        print("="*70 + "\n")
        
        # Initialize RAG application
        print("📚 Initializing RAG Application...")
        app = RAGApplication(
            pdf_path=str(PDF_PATH),
            data_dir=str(PARSE_OUTPUT_DIR),
            chroma_dir=str(CHROMA_DIR),
        )
        
        # Setup pipeline
        print("⚙️  Setting up RAG pipeline...\n")
        app.setup()
        
        # Get statistics
        print("📊 Collection Statistics:")
        print("-" * 70)
        stats = app.get_collection_stats()
        for key, value in stats.items():
            print(f"  {key:25s}: {value}")
        print("-" * 70 + "\n")
        
        # Example queries
        queries = [
            "What are the main contract terms mentioned?",
            "What policies are covered in the documents?",
            "Describe any incident records found.",
        ]
        
        print("🔍 Running Example Queries:\n")
        
        for i, query in enumerate(queries, 1):
            print(f"Query {i}: {query}")
            print("-" * 70)
            
            result = app.query(query)
            
            print(f"Answer: {result['answer']}\n")
            print(f"Sources: {len(result.get('context', []))} documents retrieved\n")
            print("="*70 + "\n")
        
        print("✅ RAG Application Ready!")
        logger.info("rag_application_completed_successfully")
        
    except DocumentPortalException as exc:
        logger.exception("document_portal_exception", error=str(exc))
        print(f"\n❌ Error: {exc}\n")
        sys.exit(1)
    except Exception as exc:
        logger.exception("unexpected_exception", error=str(exc))
        print(f"\n❌ Unexpected Error: {exc}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
