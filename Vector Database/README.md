# 🗄️ Vector Database - Embedding Storage & Search

Guide to vector databases for RAG systems. Learn storage, indexing, and similarity search mechanisms.

## 📂 Contents

This folder contains documentation and learning materials for vector database concepts and implementations.

## 🎯 Vector Database Fundamentals

### What is a Vector Database?

Stores high-dimensional vectors (embeddings) with fast similarity search capability.

```
Text Document
    ↓
[Embedding Model] → [384-dim vector]
    ↓
[Vector Database] → Store & Index
    ↓
[Similarity Search] → Find nearest neighbors
```

### Key Operations

1. **Insert** - Add vectors to database
2. **Index** - Create efficient search structures
3. **Search** - Find K nearest neighbors
4. **Delete** - Remove vectors
5. **Update** - Modify vectors

## 📊 Vector Database Comparison

| Database | Type | Best For | Scale | Cost |
|----------|------|----------|-------|------|
| **Chroma** | In-memory/Local | Prototyping | Small | Free |
| **Pinecone** | Cloud/Managed | Production | Large | Paid |
| **Weaviate** | Self-hosted | Enterprise | Large | Free/Paid |
| **Milvus** | Open-source | Custom | Large | Free |
| **FAISS** | Local | Research | Medium | Free |
| **Qdrant** | Self-hosted | Production | Large | Free/Paid |

## 🏢 Popular Vector Databases

### 1. **Chroma** (Used in this project)
```python
from langchain_chroma import Chroma

vectorstore = Chroma.from_documents(
    documents=docs,
    embedding=embeddings,
    persist_directory="./data/chroma_db"
)

# Search
results = vectorstore.similarity_search(query, k=4)
```

**Advantages:**
- ✅ Easy to use
- ✅ No external service required
- ✅ Good for prototyping

**Disadvantages:**
- ❌ Limited scalability
- ❌ Single machine
- ❌ No distributed search

### 2. **Pinecone**
```python
from langchain.vectorstores import Pinecone

vectorstore = Pinecone.from_documents(
    documents=docs,
    embedding=embeddings,
    index_name="my-index"
)
```

**Advantages:**
- ✅ Fully managed (serverless)
- ✅ Scales to billions of vectors
- ✅ High availability

**Disadvantages:**
- ❌ Requires API key
- ❌ Monthly cost
- ❌ Data residency concerns

### 3. **Weaviate**
```python
from langchain.vectorstores import Weaviate

vectorstore = Weaviate.from_documents(
    documents=docs,
    embedding=embeddings,
    client=client
)
```

**Advantages:**
- ✅ Self-hosted (control)
- ✅ GraphQL interface
- ✅ Built-in semantics

**Disadvantages:**
- ❌ Requires deployment
- ❌ More complex setup
- ❌ Maintenance overhead

### 4. **Milvus**
```python
from langchain.vectorstores import Milvus

vectorstore = Milvus.from_documents(
    documents=docs,
    embedding=embeddings,
    connection_args={"host": "localhost", "port": 19530}
)
```

**Advantages:**
- ✅ Open-source
- ✅ Distributed architecture
- ✅ High performance

**Disadvantages:**
- ❌ Complex deployment
- ❌ Steep learning curve
- ❌ Requires multiple services

## 🔍 Similarity Search Methods

### Cosine Similarity
Most common for embeddings
```
similarity = dot_product(v1, v2) / (||v1|| * ||v2||)
Result: [-1, 1] where 1 = identical
```

### Euclidean Distance
Geometric distance in vector space
```
distance = sqrt(sum((v1[i] - v2[i])^2))
Result: [0, ∞) where 0 = identical
```

### Dot Product
Fast similarity metric
```
score = dot_product(v1, v2)
```

## 🗂️ Data Management

### Persistence
```python
# Chroma persists to disk
vectorstore = Chroma(
    persist_directory="./data/chroma_db",
    embedding_function=embeddings
)
```

### Metadata Storage
```python
# Store document metadata with vectors
doc = Document(
    page_content="...",
    metadata={
        "source": "file.pdf",
        "page": 1,
        "date": "2026-11-02"
    }
)
```

### Filtering
```python
# Search with metadata filters
results = vectorstore.similarity_search(
    query="What is RAG?",
    k=4,
    filter={"source": "rag_paper.pdf"}
)
```

## 📈 Scalability Considerations

### Small Scale (< 100K vectors)
- ✅ Use: Chroma, FAISS, local storage
- Size: Single machine sufficient
- Cost: Free or minimal

### Medium Scale (100K - 10M vectors)
- ✅ Use: Milvus, Weaviate, Qdrant
- Size: Multi-machine cluster
- Cost: Moderate (self-hosted)

### Large Scale (> 10M vectors)
- ✅ Use: Pinecone, Weaviate Cloud, Milvus Cloud
- Size: Distributed, managed service
- Cost: High (pay-per-query)

## ⚙️ Performance Optimization

### Batch Indexing
```python
# Index documents in batches
batch_size = 1000
for i in range(0, len(docs), batch_size):
    batch = docs[i:i+batch_size]
    vectorstore.add_documents(batch)
```

### Dimensionality Reduction
- Use smaller embedding models (384-dim vs 1536-dim)
- Trade-off: Speed vs accuracy

### Index Types
- Flat: Exhaustive search (slow, accurate)
- IVF: Inverted index (fast, approximate)
- HNSW: Hierarchical (balanced)
- Quantization: Compressed vectors

## 🔒 Production Considerations

### Backup & Recovery
```python
# Persist vector store
vectorstore.persist()

# Restore from disk
vectorstore = Chroma(persist_directory="...")
```

### Monitoring
- Track indexing latency
- Monitor search performance
- Alert on capacity thresholds

### Security
- Encrypt vectors at rest
- Use authentication
- Control access to embeddings

## 🚀 Architecture in RAG System

```
Documents → Chunking → Embeddings → Vector DB → Retrieval → LLM → Answer
                                         ↓
                                    Similarity
                                      Search
                                        ↓
                                   Return Top-K
```

### In Our Project (src/ingestion.py)

```python
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

# Initialize embeddings
embeddings = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
)

# Create/load vector store
vector_store = Chroma.from_documents(
    documents=split_docs,
    embedding=embeddings,
    persist_directory="data/chroma_vectorstore"
)

# Create retriever
retriever = vector_store.as_retriever(search_kwargs={"k": 4})
```

## 📝 When to Migrate

**Stay with Chroma when:**
- Prototype/development
- Single machine setup
- < 100K documents
- Low query volume

**Migrate to Production DB when:**
- > 100K documents
- High query volume (> 1000 QPS)
- Need high availability
- Multi-user access

---

**Used in:** `src/ingestion.py` - DocumentIngestionPipeline
**Stored at:** `data/chroma_vectorstore/` - Persistent storage
