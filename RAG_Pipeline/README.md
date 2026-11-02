# 🔗 RAG Pipeline - End-to-End Retrieval Architecture

Complete implementation of Retrieval-Augmented Generation pipeline. Learn the full workflow from document ingestion to answer generation.

## 📂 Contents

- **RAG_Pipeline.ipynb** - Complete RAG pipeline implementation and walkthrough

## 🏗️ RAG Architecture Overview

```
Documents
    ↓
[Data Parsing] → Extract text, images, tables
    ↓
[Chunking] → Split into manageable pieces
    ↓
[Embeddings] → Convert to vector representations
    ↓
[Vector Store] → Store embeddings (Chroma, Pinecone, etc.)
    ↓
[User Query] ← 
    ↓
[Retriever] → Find relevant documents
    ↓
[Prompt Formatting] → Combine query + context
    ↓
[LLM] → Generate answer using retrieved context
    ↓
[Answer + Sources] → Return to user
```

## 🔄 Pipeline Components

### 1. **Ingestion Pipeline** (`src/ingestion.py`)
```python
from src.ingestion import DocumentIngestionPipeline

pipeline = DocumentIngestionPipeline(
    chroma_persist_dir="data/chroma_vectorstore",
    chunk_size=1000,
    chunk_overlap=200,
    embedding_model="all-MiniLM-L6-v2"
)

vector_store = pipeline.ingest_documents(documents)
```

**Responsibilities:**
- Split documents into chunks
- Create embeddings
- Store in vector database
- Manage metadata

### 2. **Retrieval** (`src/retriever.py`)
```python
from src.retriever import ChromaRetriever

retriever = ChromaRetriever(
    chroma_persist_dir="data/chroma_vectorstore",
    embedding_model="all-MiniLM-L6-v2"
)

docs = retriever.retrieve(query="What is X?", k=4)
```

**Responsibilities:**
- Query embedding creation
- Similarity search
- Return top-k documents
- Score results

### 3. **Generation** (`src/generation.py`)
```python
from src.generation import RAGGenerator

generator = RAGGenerator(
    retriever=retriever,
    llm=llm
)

answer = generator.generate(query="What is X?")
```

**Responsibilities:**
- Format prompt with context
- Call LLM
- Parse response
- Include source attribution

## 🔀 Retrieval Strategies

### Basic Similarity Search
- Simple cosine similarity on embeddings
- Fast, works for most use cases
- Default k=4

### With Relevance Scores
```python
results = retriever.retrieve_with_scores(query, k=4)
# Returns: [(Document, score), ...]
```

### Advanced Techniques

#### Sentence Window Retrieval
- Index small chunks
- Retrieve with surrounding context
- Better narrative flow

#### Parent Document Retrieval
- Small chunks for precise retrieval
- Return larger parent document
- Balances precision and context

#### Hybrid Retrieval
- Combine dense (embeddings) + sparse (BM25)
- Gets both semantic and keyword matches

## 🚀 Complete Workflow

```python
# Step 1: Parse documents
from src.data_parsing import MultimodalPDFParser
parser = MultimodalPDFParser()
documents = parser.parse_pdf("input.pdf")

# Step 2: Ingest into vector store
from src.ingestion import DocumentIngestionPipeline
pipeline = DocumentIngestionPipeline()
vector_store = pipeline.ingest_documents(documents)

# Step 3: Create retriever
from src.retriever import ChromaRetriever
retriever = ChromaRetriever()

# Step 4: Generate answers
from src.generation import RAGGenerator
generator = RAGGenerator(retriever=retriever, llm=llm)

# Step 5: Get answer
answer = generator.generate("Your question here")
```

## ⚙️ Configuration Parameters

| Component | Parameter | Default | Impact |
|-----------|-----------|---------|--------|
| Chunking | chunk_size | 1000 | Larger = more context, fewer chunks |
| Chunking | chunk_overlap | 200 | Prevents context loss at boundaries |
| Embeddings | model | all-MiniLM-L6-v2 | Quality of semantic search |
| Retrieval | k | 4 | Number of documents returned |
| LLM | temperature | 0.0 | Deterministic (0) vs creative (1.0) |
| LLM | model | gpt-oss-20b | Generation quality/speed |

## 📊 Performance Optimization

### Faster Retrieval
- Reduce chunk size
- Use simpler embedding model
- Implement caching

### Better Quality
- Increase k (retrieve more docs)
- Use advanced chunking (parent doc)
- Implement reranking

### Cost Optimization
- Use smaller LLM
- Batch queries
- Cache embeddings

## 🐛 Debugging Pipeline

1. **Check parsing**: Verify extracted documents have correct content
2. **Check embeddings**: Ensure similarity search returns relevant docs
3. **Check prompt**: Review formatted prompt sent to LLM
4. **Check response**: Test LLM directly with same prompt

## 📈 Monitoring

Track metrics:
- Retrieval latency
- LLM latency
- Total response time
- Retrieved document relevance
- Answer accuracy (if ground truth available)

---

**Entry Point:** `ui/app.py` - Full Streamlit interface with UI
**Core Logic:** `src/generation.py` - RAGGenerator orchestrates the pipeline
