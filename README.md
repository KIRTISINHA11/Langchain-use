# 🧠 Complete Multimodal RAG System - Learning & Production

A comprehensive **Retrieval-Augmented Generation (RAG)** platform with complete learning materials and production-ready implementation. Covers everything from PDF parsing to LLM-powered question-answering with text, images, and tables.

---

## 🎯 What's Inside

### 📚 **6 Learning Material Folders**

Master RAG concepts with in-depth tutorials and implementations:

#### 1. **[Chunking](./Chunking)** 📖
Document segmentation strategies for optimal retrieval
- Fixed-size chunking
- Recursive character chunking  
- Sentence window retrieval
- Parent document retrieval
- Semantic chunking

**Files:** Notebooks + README with comparisons & best practices

#### 2. **[Data Parsing](./Data%20Parsing)** 🔍
PDF & document extraction techniques
- PyMuPDF (fitz) - Fast text/image extraction
- PDFPlumber - Advanced table extraction
- Docling - Complex layout parsing
- LlamaParser - LLM-powered parsing

**Files:** 4 detailed notebooks covering each technique

#### 3. **[Prompting](./Prompting)** 🎯
LLM prompt engineering for RAG
- Zero-shot & few-shot prompting
- Chain-of-thought strategies
- RAG-specific prompt templates
- Output formatting techniques

**Files:** Notebook + JSON prompt library

#### 4. **[RAG_Pipeline](./RAG_Pipeline)** 🔗
End-to-end RAG architecture
- Complete workflow walkthrough
- Component integration
- Configuration optimization
- Performance tuning

**Files:** Comprehensive notebook with full examples

#### 5. **[Retriever](./Retriever)** 🔎
Document search & retrieval strategies
- Basic similarity search
- Hybrid retrieval (dense + sparse)
- Query transformation
- Reranking techniques
- Contextual compression

**Files:** Basic + advanced notebooks

#### 6. **[Vector Database](./Vector%20Database)** 🗄️
Embedding storage & similarity search
- Chroma (used in production)
- Pinecone, Weaviate, Milvus comparison
- Similarity metrics (cosine, euclidean, dot product)
- Scaling strategies

**Files:** README with implementation guide

---

### 🔧 **Production Implementation**

#### **[Langchain-use](./Langchain-use)** - Complete RAG System

**Core Modules:**
- `src/data_parsing.py` - Multimodal PDF parser (text, images, tables)
- `src/ingestion.py` - Document chunking & vector embedding pipeline
- `src/retriever.py` - Chroma vector store retrieval
- `src/generation.py` - LLM-powered answer generation
- `ui/app.py` - Streamlit web interface

**Infrastructure:**
- `logger/` - Structured logging system
- `exception/` - Custom error handling
- `prompt_library/` - Reusable LLM prompts
- `data/` - PDFs, embeddings, parsed outputs

**Features:**
✅ Extract text, images, tables from PDFs
✅ Multiple chunking strategies
✅ HuggingFace embeddings (all-MiniLM-L6-v2)
✅ Chroma vector database
✅ ChatGroq LLM integration
✅ Streamlit dashboard
✅ Structured logging & error handling
✅ 37 extracted images as proof-of-work

---

## 🚀 Quick Start

### **Installation**

```bash
# Clone repository
git clone https://github.com/KIRTISINHA11/Langchain-use.git
cd Langchain-use

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r Langchain-use/requirements.txt

# Configure API keys
echo "GROQ_API_KEY=your_key_here" > .env
```

### **Run the Application**

```bash
# Launch Streamlit UI
streamlit run Langchain-use/ui/app.py
```

Access at: `http://localhost:8501`

### **Parse a PDF**

```python
from Langchain-use.src.data_parsing import MultimodalPDFParser

parser = MultimodalPDFParser(
    pdf_path="path/to/document.pdf",
    output_dir="output_folder"
)

result = parser.parse(save_output=True)
documents = result["documents"]  # LangChain docs
images = result["page_image_dir"]  # Full pages
```

### **Query with RAG**

```python
from Langchain-use.src.generation import RAGGenerator
from Langchain-use.src.retriever import ChromaRetriever

# Initialize
retriever = ChromaRetriever(
    chroma_persist_dir="Langchain-use/data/chroma_vectorstore"
)

generator = RAGGenerator(retriever=retriever, llm=llm)

# Ask a question
answer = generator.generate("What is the main topic?")
```

---

## 📊 Technology Stack

**PDF Processing:**
- PyMuPDF (fitz) - Text & image extraction
- pdfplumber - Table extraction
- Docling - Complex layout parsing

**NLP & Embeddings:**
- LangChain - Document processing
- HuggingFace Embeddings - all-MiniLM-L6-v2 (384-dim)
- Sentence Transformers

**Vector Database:**
- Chroma - Persistent storage & retrieval
- Support for Pinecone, Weaviate, Milvus

**LLM:**
- ChatGroq - Fast inference (gpt-oss-20b)
- Support for Claude, GPT-4, Gemini

**Web UI:**
- Streamlit - Interactive dashboard
- Real-time Q&A interface

**Infrastructure:**
- Python 3.10+
- Custom logging system
- Error handling framework

---

## 📁 Repository Structure

```
Langchain-use/
├── Chunking/                          # Segmentation strategies
│   ├── Chunking_Methods.ipynb
│   ├── Chunking_Masterclass_Practical.ipynb
│   └── README.md
│
├── Data Parsing/                      # Extraction techniques
│   ├── data_parsing_part1_langchain_data_loaders.ipynb
│   ├── data_parsing_part2_pymupdf_pdfplumber.ipynb
│   ├── data_parsing_part3_docling.ipynb
│   ├── data_parsing_part4_llama_parser.ipynb
│   └── README.md
│
├── Prompting/                         # Prompt engineering
│   ├── prompting.ipynb
│   ├── prompt.json
│   ├── prompts.json
│   └── README.md
│
├── RAG_Pipeline/                      # Complete architecture
│   ├── RAG_Pipeline.ipynb
│   └── README.md
│
├── Retriever/                         # Search strategies
│   ├── retriever.ipynb
│   ├── retriever_advance.ipynb
│   └── README.md
│
├── Vector Database/                   # Storage & retrieval
│   ├── Chroma-DB/Chroma_db.ipynb
│   └── README.md
│
├── Langchain-use/                     # Production system
│   ├── src/
│   │   ├── data_parsing.py            # PDF parser
│   │   ├── ingestion.py               # Chunking & embedding
│   │   ├── retriever.py               # Vector search
│   │   ├── generation.py              # LLM generation
│   │   └── README.md
│   ├── ui/
│   │   ├── app.py                     # Streamlit dashboard
│   │   └── README.md
│   ├── logger/
│   │   ├── custom_logger.py
│   │   └── README.md
│   ├── exception/
│   │   ├── custom_exception.py
│   │   └── README.md
│   ├── prompt_library/
│   │   ├── prompt.py
│   │   └── README.md
│   ├── data/
│   │   ├── uploads/                   # PDFs
│   │   ├── parsed_pdf_output/         # Extracted content
│   │   │   ├── extracted_images/      # 13 images
│   │   │   └── page_images/           # 24 page renders
│   │   └── README.md
│   ├── README.md
│   └── requirements.txt
│
├── .gitignore
├── requirements.txt
└── README.md (this file)
```

---

## 🎓 Learning Path

**Start Here:**
1. **[Vector Database](./Vector%20Database)** - Understand embeddings
2. **[Data Parsing](./Data%20Parsing)** - Extract content from PDFs
3. **[Chunking](./Chunking)** - Optimize document segmentation
4. **[RAG_Pipeline](./RAG_Pipeline)** - Understand full workflow
5. **[Retriever](./Retriever)** - Master search strategies
6. **[Prompting](./Prompting)** - Craft effective prompts
7. **[Langchain-use](./Langchain-use)** - Build production system

---

## 🔬 Key Techniques Covered

### Chunking Strategies
- Fixed-size (simple, fast)
- Recursive character (balanced)
- Sentence window (context-aware)
- Parent document (hierarchical)
- Semantic (meaning-based)

### Retrieval Techniques
- Similarity search (cosine, euclidean)
- Hybrid retrieval (dense + BM25)
- Query transformation (multi-query, decomposition)
- Reranking (LLM-based relevance)
- Contextual compression

### Vector Databases
- Chroma (local, prototyping)
- Pinecone (cloud, production)
- Weaviate (self-hosted, enterprise)
- Milvus (distributed, open-source)

### LLM Integration
- Claude Vision - Multimodal understanding
- GPT-4V - Visual reasoning
- Gemini - Multimodal capabilities
- ChatGroq - Fast, efficient inference

---

## 📊 Production Features

✅ **Multimodal Processing**
- Extract text, images, tables from PDFs
- Vision LLM support for image understanding
- Hybrid text + image retrieval

✅ **Robust Pipeline**
- Error handling with custom exceptions
- Structured logging with multiple levels
- Configuration management
- Persistent vector store

✅ **User Interface**
- Streamlit web dashboard
- Real-time PDF upload & parsing
- Interactive Q&A interface
- Document preview

✅ **Scalability**
- Modular architecture
- Support for multiple vector databases
- Batch processing capability
- Efficient caching

---

## 🎯 Use Cases

1. **Document Q&A** - Ask questions about PDFs
2. **Contract Analysis** - Extract & understand terms
3. **Research** - Search across multiple documents
4. **Knowledge Base** - Build searchable archives
5. **Legal Review** - Analyze policies & agreements
6. **Training Data** - Generate embeddings for ML

---

## 📝 Example: Complete RAG Query

```python
from Langchain-use.src.data_parsing import MultimodalPDFParser
from Langchain-use.src.ingestion import DocumentIngestionPipeline
from Langchain-use.src.generation import RAGGenerator

# Step 1: Parse PDF
parser = MultimodalPDFParser(
    pdf_path="document.pdf",
    output_dir="output"
)
result = parser.parse(save_output=True)
documents = result["documents"]

# Step 2: Ingest into vector store
pipeline = DocumentIngestionPipeline(
    chroma_persist_dir="chroma_db"
)
vector_store = pipeline.ingest_documents(documents)

# Step 3: Generate answer
generator = RAGGenerator(
    retriever=pipeline.get_retriever(),
    llm=pipeline.get_llm()
)

answer = generator.generate("What are the key points?")
print(answer)
```

---

## 🐛 Troubleshooting

**Q: ModuleNotFoundError for PyMuPDF?**
- Ensure lazy-loading is enabled in data_parsing.py
- PyMuPDF imported inside methods, not at module level

**Q: Chroma vector store not persisting?**
- Check `chroma_persist_dir` has write permissions
- Verify database files in directory

**Q: Slow retrieval performance?**
- Reduce chunk size
- Use simpler embedding model
- Implement caching for frequent queries

**Q: LLM API errors?**
- Verify GROQ_API_KEY in .env
- Check rate limits
- Monitor API status

---

## 📚 Documentation

- **[Langchain-use/README.md](./Langchain-use/README.md)** - Production system
- **[Chunking/README.md](./Chunking/README.md)** - Segmentation guide
- **[Data Parsing/README.md](./Data%20Parsing/README.md)** - Extraction techniques
- **[Prompting/README.md](./Prompting/README.md)** - Prompt engineering
- **[RAG_Pipeline/README.md](./RAG_Pipeline/README.md)** - Architecture overview
- **[Retriever/README.md](./Retriever/README.md)** - Search strategies
- **[Vector Database/README.md](./Vector%20Database/README.md)** - Database guide

---

## 🔗 External Resources

- [LangChain Documentation](https://python.langchain.com/)
- [Chroma DB Guide](https://docs.trychroma.com/)
- [HuggingFace Embeddings](https://huggingface.co/spaces/mteb/leaderboard)
- [Claude Vision API](https://docs.anthropic.com/en/api/vision)
- [PyMuPDF Docs](https://pymupdf.readthedocs.io/)

---

## 👥 Contributors

- **KIRTISINHA11** - Author
- **varshaZinnia** - Collaborator

---

## 📄 License

MIT License - See [LICENSE](./LICENSE) file

---

## 🚀 Get Started

1. **Clone:** `git clone https://github.com/KIRTISINHA11/Langchain-use.git`
2. **Install:** `pip install -r Langchain-use/requirements.txt`
3. **Configure:** Add `GROQ_API_KEY` to `.env`
4. **Run:** `streamlit run Langchain-use/ui/app.py`
5. **Explore:** Check individual folder READMEs for deep dives

---

**Ready to build multimodal RAG systems? Start exploring! 🎓🚀**

Last Updated: November 2, 2026
