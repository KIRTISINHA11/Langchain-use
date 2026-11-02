# 💾 data/ - Project Data Directory

Storage for PDFs, parsed outputs, and vector embeddings.

## 📂 Subdirectories

### uploads/
User-uploaded PDF files for processing.
```
uploads/
├── document1.pdf
├── document2.pdf
└── ...
```

### parsed_pdf_output/
Extracted content from PDFs after parsing.
```
parsed_pdf_output/
├── document1/
│   ├── page_records.json      # Text per page
│   ├── image_records.json     # Extracted images metadata
│   ├── table_records.json     # Tables in markdown
│   ├── extracted_images/      # Embedded images
│   └── page_images/           # Full page renders
├── document2/
│   └── ...
```

### chroma_vectorstore/
Persistent vector database with embeddings.
```
chroma_vectorstore/
├── index/
├── db.sqlite3
└── ...
```

## 🔄 Data Flow

1. **Raw PDFs** → `uploads/`
2. **Parse** → `parsed_pdf_output/`
3. **Embed** → `chroma_vectorstore/`

## 💾 Storage Management

- Keep only necessary PDFs
- Parsed outputs auto-generated from PDFs
- Vector database can be regenerated

---

**Managed by RAG pipeline**
