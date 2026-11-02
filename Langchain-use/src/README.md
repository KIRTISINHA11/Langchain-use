# 📦 src/ - Core RAG Pipeline Modules

Production-grade modules for multimodal document processing and retrieval-augmented generation.

## 📂 Files Overview

### 1. **parsing.py** - PDF Document Extraction
**Purpose:** Extract text, images, tables, and metadata from PDF documents

**Key Techniques:**
- **PyMuPDF (fitz)** - Text extraction, page rendering, embedded image extraction
- **pdfplumber** - Table detection and extraction with high accuracy
- **PIL/Pillow** - Image processing and optimization
- **LangChain Documents** - Standard document format for RAG pipeline

**Class: MultimodalPDFParser**

```python
parser = MultimodalPDFParser(
    pdf_path="document.pdf",
    output_dir="parsed_output",
    render_scale=2.0  # Page rendering quality
)

result = parser.parse(save_output=True)
# Returns: {
#   "pages": [...],           # Text from each page
#   "images": [...],          # Extracted images
#   "tables": [...],          # Tables in markdown
#   "documents": [...]        # LangChain Documents
# }
```

**Output Structure:**
```
parsed_output/
├── page_records.json         # Text + metadata per page
├── image_records.json        # Image references + OCR
├── table_records.json        # Table content in markdown
├── extracted_images/         # Embedded diagrams, charts
├── page_images/              # Full-page renders
└── rag_ready_documents.md    # Combined markdown export
```

---

### 2. **ingestion.py** - Document Chunking & Embedding Pipeline
**Purpose:** Convert parsed documents into vector embeddings and store in Chroma

**Key Techniques:**

#### **Chunking Strategies**

| Strategy | Code | Chunk Size | Overlap | Use Case |
|----------|------|-----------|---------|----------|
| **Recursive Character** | `RecursiveCharacterTextSplitter` | 1000 | 200 | General text |
| **Sentence-based** | Custom implementation | ~sentence length | Small | Precise retrieval |
| **Parent-Document** | Built-in LangChain | Parent: 2000, Child: 400 | 100/50 | Large documents |

#### **Embedding Model**
- **HuggingFace: all-MiniLM-L6-v2**
  - 384-dimensional embeddings
  - Fast inference
  - Good semantic understanding
  - ~12MB model size

#### **Vector Database**
- **Chroma** (Local, persistent)
  - SQLite-backed storage
  - Cosine similarity search
  - Metadata filtering support
  - No external dependencies

**Class: DocumentIngestionPipeline**

```python
pipeline = DocumentIngestionPipeline(
    chroma_persist_dir="./chroma_db",
    embedding_model="all-MiniLM-L6-v2",
    chunk_size=1000,
    chunk_overlap=200,
    groq_model="openai/gpt-oss-20b",
    groq_temperature=0.0
)

# Ingest documents
pipeline.ingest_documents(
    documents=parsed_docs,
    collection_name="pdf_documents",
    split_documents=True  # Auto-chunk
)

# Retrieve
retriever = pipeline.get_retriever({"k": 4})
results = retriever.invoke("your query")

# Get LLM
llm = pipeline.get_llm()
```

---

### 3. **retrieval.py** - Vector Store Retrieval
**Purpose:** Retrieve relevant documents from Chroma vector database

**Key Techniques:**
- **Similarity Search** - Cosine similarity in embedding space
- **Similarity with Scores** - Ranked results with confidence
- **Metadata Filtering** - Filter by page number, content type, etc.

**Class: ChromaRetriever**

```python
retriever = ChromaRetriever(
    chroma_persist_dir="./chroma_db",
    collection_name="pdf_documents",
    embedding_model="all-MiniLM-L6-v2"
)

# Get top-4 similar documents
results = retriever.retrieve(query="contract terms", k=4)

# With relevance scores
results_with_scores = retriever.retrieve_with_scores(
    query="contract terms",
    k=4
)
# Returns: [(Document, similarity_score), ...]
```

**Retrieval Strategies Implemented:**
- Dense (embedding-based) retrieval
- BM25 sparse retrieval (can be added)
- Reciprocal Rank Fusion (future)
- Contextual compression (future)

---

### 4. **generation.py** - LLM Answer Generation
**Purpose:** Generate context-aware answers using retrieved documents

**Key Techniques:**
- **Prompt Engineering** - Structured system + user prompts
- **Context Formatting** - Organize retrieved docs for clarity
- **Temperature Control** - 0.0 for deterministic responses
- **Token Limiting** - Prevent runaway generations

**Class: RAGGenerator**

```python
generator = RAGGenerator(
    chroma_persist_dir="./chroma_db",
    collection_name="pdf_documents",
    groq_model="openai/gpt-oss-20b",
    groq_temperature=0.0
)

# Generate answer
result = generator.generate_answer(
    query="What are the contract terms?",
    k=4  # Retrieve top-4 docs
)
# Returns: {
#   "answer": "Based on the documents...",
#   "retrieved_docs": [...],
#   "doc_count": 4
# }
```

**LLM: ChatGroq**
- Model: `openai/gpt-oss-20b`
- Speed: Fast inference
- Cost: Very affordable
- Quality: Good for RAG tasks

---

### 5. **vision_rag.py** - Vision LLM Integration
**Purpose:** Enable analysis of extracted images with vision models

**Supported Vision LLMs:**
- **Claude Vision** (Anthropic)
- **GPT-4V** (OpenAI)
- **Gemini Vision** (Google)

**Class: VisionRAGIntegration**

```python
# Encode image
image_data = VisionRAGIntegration.encode_image_to_base64("page_001.png")

# Create Claude Vision message
msg = VisionRAGIntegration.create_claude_vision_message(
    image_path="page_001.png",
    query="What does this diagram show?"
)

# Create GPT-4V message
msg = VisionRAGIntegration.create_gpt4v_vision_message(
    image_path="page_001.png",
    query="Extract all text from this image"
)

# Create Gemini message
msg = VisionRAGIntegration.create_gemini_vision_message(
    image_path="page_001.png",
    query="Describe the layout"
)
```

---

## 🔄 Complete Pipeline Flow

```
1. PARSING (parsing.py)
   Input: PDF file
   Process: Extract text, images, tables
   Output: LangChain Documents + metadata

2. INGESTION (ingestion.py)
   Input: Documents
   Process: Chunk → Embed → Store
   Output: Chroma vector database

3. RETRIEVAL (retrieval.py)
   Input: User query
   Process: Embed query → Similarity search
   Output: Top-k relevant documents

4. GENERATION (generation.py)
   Input: Query + Retrieved docs
   Process: Format context → LLM call
   Output: Answer text

5. VISION (vision_rag.py)
   Input: Extracted images
   Process: Vision LLM analysis
   Output: Image descriptions/analysis
```

---

## 📊 Configuration Guide

### Chunk Size Selection

```python
# Small chunks (400 tokens)
# ✓ More precise retrieval
# ✗ More total chunks
# ✓ Lower latency

# Medium chunks (1000 tokens) - RECOMMENDED
# ✓ Good balance
# ✓ Reasonable context window

# Large chunks (2000+ tokens)
# ✓ More context
# ✗ Less precise
# ✗ Slower retrieval
```

### Embedding Model Comparison

| Model | Size | Speed | Quality | Use |
|-------|------|-------|---------|-----|
| all-MiniLM-L6-v2 | 22M | Fast | Good | Default ✓ |
| sentence-transformers | 420M | Medium | Very Good | High quality |
| OpenAI ada | - | Slow | Excellent | Premium |

### LLM Model Selection

| Model | Speed | Cost | Quality | Context |
|-------|-------|------|---------|---------|
| Groq 20B | Fast | Cheap | Good | 8K |
| Claude 3.5 | Medium | Medium | Excellent | 200K |
| GPT-4 | Slow | Expensive | Excellent | 8K |

---

## 🧪 Testing

### Test Parsing

```bash
python src/parsing.py
```

### Test Ingestion

```python
from src.ingestion import DocumentIngestionPipeline

pipeline = DocumentIngestionPipeline(
    chroma_persist_dir="./test_chroma"
)
# Check for errors during initialization
```

### Test Retrieval

```python
from src.retrieval import ChromaRetriever

retriever = ChromaRetriever(
    chroma_persist_dir="./test_chroma"
)
results = retriever.retrieve("test query", k=4)
assert len(results) > 0
```

---

## 🚀 Performance Tips

1. **Parallel Batch Processing** - Process multiple PDFs at once
2. **Chunk Reuse** - Cache embeddings between runs
3. **Top-K Tuning** - Start with k=4, adjust based on quality
4. **Temperature Control** - Use 0.0 for consistency
5. **Image Optimization** - Reduce resolution before vision LLM

---

## 📚 Advanced Techniques

### Hybrid Retrieval (Planned)
Combine sparse (BM25) + dense (embeddings) retrieval for best results.

### Multi-hop Reasoning
Use retrieved answers to ask follow-up questions.

### Contextual Compression
Extract only relevant portions from long retrieved documents.

### Query Transformation
Rewrite queries for better retrieval (HyDE, decomposition).

---

## 🤝 Dependencies

```
langchain>=0.1.0
langchain-core>=0.1.0
langchain-chroma>=1.1.0
langchain-huggingface>=1.2.0
langchain-groq>=1.1.0
chromadb>=0.4.0
sentence-transformers>=2.2.0
pymupdf>=2.0
pdfplumber>=0.10.3
```

---

**Built with ❤️ for intelligent document understanding**
