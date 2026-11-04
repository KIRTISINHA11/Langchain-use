from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
import sys
from pathlib import Path

# Add parent directories to path for imports (go up 3 levels to Langchain-use)
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.parsing import MultimodalPDFParser
from src.ingestion import DocumentIngestionPipeline
from src.generation import RAGGenerator
from src.retriever import ChromaRetriever

app = FastAPI(title="ZSearch API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global state
documents_store = {}
ingestion_pipeline = None
rag_generator = None
chroma_persist_dir = "data/chroma_vectorstore"

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    answer: str
    sources: Optional[List[dict]] = None
    confidence: Optional[float] = None

@app.on_event("startup")
async def startup_event():
    """Initialize RAG pipeline on startup"""
    global ingestion_pipeline, rag_generator
    try:
        ingestion_pipeline = DocumentIngestionPipeline(
            chroma_persist_dir=chroma_persist_dir
        )
        rag_generator = RAGGenerator(chroma_persist_dir=chroma_persist_dir)
        print("✅ RAG pipeline initialized successfully")
    except Exception as e:
        print(f"⚠️ Warning: RAG pipeline initialization failed: {e}")
        print("Some features may not work until a document is uploaded")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "rag_pipeline": "ready" if ingestion_pipeline else "initializing",
        "documents": len(documents_store)
    }

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """Upload and process a document"""
    global ingestion_pipeline, rag_generator

    if file.content_type not in ["application/pdf", "text/csv"]:
        raise HTTPException(
            status_code=400,
            detail="Only PDF and CSV files are supported"
        )

    try:
        # Create temporary file
        temp_path = f"temp_{file.filename}"
        with open(temp_path, "wb") as f:
            content = await file.read()
            f.write(content)

        # Parse document
        parser = MultimodalPDFParser(
            pdf_path=temp_path,
            output_dir="data/parsed_pdf_output"
        )

        result = parser.parse(save_output=True)
        documents = result.get("documents", [])

        # Ingest into vector store
        if ingestion_pipeline:
            vector_store = ingestion_pipeline.ingest_documents(documents)

            # Re-initialize generator with new documents
            rag_generator = RAGGenerator(chroma_persist_dir=chroma_persist_dir)

        # Store metadata
        documents_store[file.filename] = {
            "filename": file.filename,
            "size": len(content),
            "document_count": len(documents)
        }

        # Cleanup
        if os.path.exists(temp_path):
            os.remove(temp_path)

        return {
            "filename": file.filename,
            "status": "uploaded",
            "documents_processed": len(documents)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query", response_model=QueryResponse)
async def query_documents(request: QueryRequest):
    """Query uploaded documents"""
    global rag_generator

    if not documents_store:
        raise HTTPException(
            status_code=400,
            detail="No documents uploaded yet. Please upload a document first."
        )

    if not rag_generator:
        raise HTTPException(
            status_code=500,
            detail="RAG system not initialized"
        )

    try:
        # Generate answer using RAG
        result = rag_generator.generate_answer(request.question)

        # Extract answer and sources
        answer = result.get("answer", "")
        retrieved_docs = result.get("retrieved_docs", [])

        # Format sources
        sources = None
        if retrieved_docs:
            sources = [
                {
                    "document": doc.metadata.get("source", "unknown") if hasattr(doc, 'metadata') else "unknown",
                    "page": doc.metadata.get("page", None) if hasattr(doc, 'metadata') else None
                }
                for doc in retrieved_docs
            ]

        return QueryResponse(
            answer=str(answer),
            sources=sources,
            confidence=0.85
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/debug-query")
async def debug_query(request: QueryRequest):
    """Debug endpoint: show what documents are retrieved"""
    global rag_generator

    if not rag_generator:
        raise HTTPException(status_code=500, detail="RAG system not initialized")

    try:
        # Just retrieve documents without generating
        retrieved_docs = rag_generator.retriever.retrieve(request.question, k=5)

        return {
            "question": request.question,
            "retrieved_count": len(retrieved_docs),
            "documents": [
                {
                    "content": doc.page_content[:200] + "...",
                    "metadata": doc.metadata if hasattr(doc, 'metadata') else {}
                }
                for doc in retrieved_docs
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/documents")
async def list_documents():
    """List all uploaded documents"""
    return {
        "documents": documents_store,
        "count": len(documents_store)
    }

@app.post("/clear")
async def clear_documents():
    """Clear all documents and reset the system"""
    global documents_store, ingestion_pipeline, rag_generator

    try:
        documents_store.clear()

        # Reinitialize pipeline
        if os.path.exists(chroma_persist_dir):
            import shutil
            shutil.rmtree(chroma_persist_dir)

        ingestion_pipeline = DocumentIngestionPipeline(
            chroma_persist_dir=chroma_persist_dir
        )
        rag_generator = RAGGenerator(chroma_persist_dir=chroma_persist_dir)

        return {"status": "cleared"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
