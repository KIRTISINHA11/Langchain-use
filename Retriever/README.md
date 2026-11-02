# 🔎 Retriever - Document Search & Retrieval

Advanced techniques for retrieving relevant documents from vector stores. Learn different retrieval strategies and their trade-offs.

## 📂 Contents

- **retriever.ipynb** - Basic retrieval techniques and implementation
- **retriever_advance.ipynb** - Advanced retrieval strategies

## 🎯 Retrieval Fundamentals

### What is Retrieval?
Transform user query → Find most relevant documents from knowledge base

```
User Query (text)
    ↓
[Embed Query]
    ↓
[Search Vector Store]
    ↓
[Return Top-K Documents]
```

## 📚 Retrieval Types

### 1. **Similarity Search**
Find documents semantically similar to query
```python
results = retriever.retrieve(query="What is RAG?", k=4)
# Returns: [Document1, Document2, Document3, Document4]
```

**Pros:** Fast, simple, effective
**Cons:** May miss keyword-specific results

### 2. **Hybrid Retrieval**
Combine dense (embeddings) + sparse (keyword) search

```python
# Dense: Semantic similarity
dense_results = vector_store.similarity_search(query)

# Sparse: BM25 keyword matching
bm25_results = bm25_retriever.get_relevant_documents(query)

# Combine
combined = merge_results(dense_results, bm25_results)
```

**Pros:** Catches both semantic and keyword matches
**Cons:** More complex, slower

### 3. **Reranking**
Retrieve more docs, then rerank by relevance

```python
# Retrieve 20 documents
candidates = retriever.retrieve(query, k=20)

# Rerank to top 4
reranked = reranker.rerank(query, candidates, top_k=4)
```

**Pros:** Better quality results
**Cons:** Slower, requires reranker model

## 🔍 Advanced Retrieval Strategies

### Query Transformation
Improve query before retrieval

**Multi-Query:**
```python
# Generate multiple views of query
queries = [
    "What is RAG?",
    "Explain Retrieval-Augmented Generation",
    "RAG system architecture"
]
results = []
for q in queries:
    results.extend(retriever.retrieve(q))
results = deduplicate(results)
```

**Query Expansion:**
```python
# Add context to query
expanded = f"{query} AND related concepts"
```

**Decomposition:**
```python
# Break complex query into sub-queries
original: "How does RAG compare to fine-tuning?"
sub_query_1: "How does RAG work?"
sub_query_2: "How does fine-tuning work?"
sub_query_3: "Comparison of RAG and fine-tuning"
```

### Contextual Compression
Compress retrieved documents

```python
from langchain.retrievers import ContextualCompressionRetriever

compressor = LLMChainExtractor.from_llm(llm, prompt)
compressed_retriever = ContextualCompressionRetriever(
    base_compressor=compressor,
    base_retriever=retriever
)

# Returns: Only relevant parts of documents
results = compressed_retriever.get_relevant_documents(query)
```

### Sentence Window Retrieval
Small indexed chunks, retrieve with context

```python
# Index: Single sentences
# Retrieve: Sentence + window_size sentences around it

retriever = SentenceWindowNodeParser(
    window_size=3  # Get 3 sentences before/after
).get_retriever()
```

### Parent Document Retrieval
Small chunks for retrieval, return larger parent

```python
# Index: Chunks of 256 tokens
# Retrieve: Return full paragraph (1000 tokens)

retriever = ParentDocumentRetriever(
    child_splitter=child_splitter,
    parent_splitter=parent_splitter,
    vectorstore=vectorstore
)
```

## ⚡ Retrieval Performance

### Speed Comparison
| Strategy | Speed | Quality |
|----------|-------|---------|
| Cosine Similarity | ⚡⚡⚡ | ⭐⭐⭐ |
| With Filtering | ⚡⚡ | ⭐⭐⭐⭐ |
| Hybrid | ⚡ | ⭐⭐⭐⭐ |
| With Reranking | ⭐ | ⭐⭐⭐⭐⭐ |

### Optimization Tips
1. **Reduce k** - Retrieve fewer documents
2. **Use indexing** - Vectorize documents once
3. **Implement caching** - Cache frequent queries
4. **Pre-filter** - Filter by metadata first

## 🔧 Implementation

### Basic Similarity Search
```python
from src.retriever import ChromaRetriever

retriever = ChromaRetriever(
    chroma_persist_dir="data/chroma_vectorstore",
    embedding_model="all-MiniLM-L6-v2"
)

# Retrieve documents
docs = retriever.retrieve(query="What is RAG?", k=4)

# With scores
results = retriever.retrieve_with_scores(query, k=4)
# Returns: [(doc, score), ...]
```

### Search with Metadata Filtering
```python
# Retrieve only documents from specific source
results = retriever.retrieve(
    query="What is RAG?",
    k=4,
    filter={"source": "rag_paper.pdf"}
)
```

## 📊 Retrieval Evaluation

Measure effectiveness:

```python
# Precision: Are retrieved docs relevant?
precision = relevant_docs / total_retrieved

# Recall: Did we find all relevant docs?
recall = relevant_docs / total_relevant

# MRR: How high is first relevant doc?
mrr = 1 / rank_of_first_relevant

# NDCG: Ranking quality considering order
ndcg = score_based_on_relevance_and_rank
```

## 🎯 When to Use Each

| Use Case | Strategy |
|----------|----------|
| General Q&A | Cosine Similarity |
| Keyword-heavy | Hybrid Retrieval |
| Complex questions | Multi-Query |
| Long documents | Parent Document |
| Strict accuracy needed | With Reranking |

---

**Integrated in:** `src/retriever.py` - ChromaRetriever
**Used by:** `src/generation.py` - RAGGenerator
