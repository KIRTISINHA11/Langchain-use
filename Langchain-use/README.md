# 🧠 Multimodal RAG (Retrieval-Augmented Generation) with LangChain

A production-grade **Multimodal Retrieval-Augmented Generation** system that extracts and processes text, tables, and images from PDFs, then enables intelligent question-answering through semantic search and LLM integration.

## 🎯 Overview

**What it does:**
- 📄 **PDF Parsing** → Extract text, images, tables with PyMuPDF & pdfplumber
- 🗂️ **Chunking** → Multiple strategies (recursive, sentence-based, parent-document)
- 🔍 **Retrieval** → Hybrid search (BM25 + dense embeddings via Chroma)
- 🧠 **Generation** → ChatGroq LLM for context-aware answers
- 🖼️ **Multimodal** → Vision LLM support (Claude, GPT-4V, Gemini)
- 💬 **UI** → Streamlit dashboard for interactive querying

## 🚀 Quick Start

```bash
# Setup
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# Configure
echo "GROQ_API_KEY=your_key_here" > .env

# Run
streamlit run ui/app.py
```

## 📁 Folder Structure

- **src/** - Core RAG pipeline (parsing, ingestion, retrieval, generation)
- **ui/** - Streamlit web interface
- **logger/** - Structured logging system
- **exception/** - Custom exception handling
- **prompt_library/** - LLM prompts
- **data/** - PDFs and vector database

## 🔬 Key Technologies

- **PyMuPDF** - PDF text/image extraction
- **pdfplumber** - Table extraction
- **LangChain** - Document processing
- **Chroma** - Vector database
- **HuggingFace Embeddings** - Dense embeddings (all-MiniLM-L6-v2)
- **ChatGroq** - Fast LLM generation
- **Streamlit** - Web UI

## 📚 Documentation

- [src/README.md](./src/README.md) - Core modules & techniques
- [logger/README.md](./logger/README.md) - Logging system
- [exception/README.md](./exception/README.md) - Error handling
- [prompt_library/README.md](./prompt_library/README.md) - Prompts

## 🎬 Workflow

PDF → Parse → Chunk → Embed → Store → Query → Retrieve → Generate → Display

## 📝 License

MIT - See LICENSE file
