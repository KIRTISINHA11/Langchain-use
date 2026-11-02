# 💻 ui/ - Streamlit Web Interface

Interactive dashboard for document processing and Q&A.

## 📂 Files

- **app.py** - Main Streamlit application

## 🎯 Overview

**Features:**
- PDF upload/selection
- Automatic parsing
- Chroma indexing
- Interactive chat
- Source document display
- Resume-aware workflow

## 🚀 Usage

```bash
streamlit run ui/app.py
```

**Opens:** `http://localhost:8501`

## 🎬 Workflow

1. **Upload/Select PDF**
   - Choose existing PDF or upload new one
   - Checks for existing parsed artifacts

2. **Parse Document**
   - Extracts text, images, tables
   - Creates LangChain documents
   - Shows parsing progress

3. **Configure Chunking**
   - Adjust chunk size
   - Set overlap amount
   - Choose replacement strategy

4. **Index to Chroma**
   - Creates embeddings
   - Stores in vector DB
   - Shows indexing progress

5. **Chat Interface**
   - Ask questions
   - Get context-aware answers
   - View retrieved sources

## 🎨 UI Components

- **Sidebar**
  - Document selection
  - Pipeline controls
  - Configuration options
  - Document inspector

- **Main Area**
  - Chat history
  - Response with sources
  - Document details

---

**Streamlit-powered RAG interface**
