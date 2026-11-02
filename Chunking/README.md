# 📚 Chunking - Document Segmentation Strategies

Comprehensive guide to text chunking strategies for RAG systems. Learn how to split documents optimally for embedding and retrieval.

## 📂 Contents

- **Chunking_Complete_Classroom_Practical.docx** - Complete classroom practical with exercises
- **Chunking_Masterclass_Practical.ipynb** - Advanced masterclass with hands-on examples
- **Chunking_Methods.ipynb** - Detailed notebook covering all chunking techniques

## 🎯 Key Concepts Covered

### 1. **Fixed-Size Chunking**
- Simple fixed token/character splits
- Fast but context-unaware
- Use when: Quick implementation needed

```python
chunk_size = 1000
chunk_overlap = 200
```

### 2. **Recursive Character Chunking**
- Splits by progressively smaller separators
- Maintains semantic coherence
- Separators: `"\n\n" → "\n" → "." → " "`
- **Best for**: Most general-purpose RAG

### 3. **Sentence Window Retrieval**
- Chunks at sentence boundaries
- Retrieves sentences + surrounding context window
- Preserves narrative flow
- Better context for QA tasks

### 4. **Parent Document Retrieval**
- Small chunks for retrieval
- Returns larger parent context
- Balances precision (small chunks) with context (large parent)
- Excellent for dense documents

### 5. **Semantic Chunking**
- Splits based on content meaning
- Uses embeddings to detect semantic boundaries
- Most sophisticated approach
- Requires embedding model

## 🔧 Configuration

### Chunk Size Selection
```
Small (256-512):  High precision, less context
Medium (1000):    Balanced, recommended
Large (2048+):    More context, less specificity
```

### Overlap Strategy
- **Typical**: 10-20% of chunk size
- Overlap: 200 chars for 1000 char chunks
- Ensures no lost context at boundaries

## 📊 Comparison

| Method | Speed | Context | Quality |
|--------|-------|---------|---------|
| Fixed-Size | ⚡⚡⚡ | ⭐⭐ | ⭐⭐ |
| Recursive | ⚡⚡ | ⭐⭐⭐ | ⭐⭐⭐ |
| Sentence Window | ⚡⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| Parent Document | ⚡⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Semantic | ⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

## 🚀 Implementation in Langchain

```python
from langchain_text_splitters import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    separators=["\n\n", "\n", ".", " ", ""]
)

chunks = splitter.split_documents(documents)
```

## 📝 When to Use Each

- **PDFs with structure**: Sentence Window or Parent Document
- **Web articles**: Recursive Character Chunking
- **Books/papers**: Semantic Chunking
- **Quick prototypes**: Fixed-Size

---

**Integrated in:** `src/ingestion.py` - DocumentIngestionPipeline
