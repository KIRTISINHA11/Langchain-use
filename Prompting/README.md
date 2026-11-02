# 🎯 Prompting - LLM Prompt Engineering

Comprehensive prompt templates and strategies for RAG systems. Optimize LLM outputs with structured prompting.

## 📂 Contents

- **prompting.ipynb** - Interactive prompting techniques and examples
- **prompt.json** - Single prompt template configuration
- **prompts.json** - Library of reusable prompt templates

## 🎨 Prompting Strategies

### 1. **Zero-Shot Prompting**
Direct question without examples
```
"Answer the following question based on the provided context:
Question: {query}
Context: {context}"
```

### 2. **Few-Shot Prompting**
Include examples to guide output
```
"Answer questions like these examples:
Example 1: Q: {q1} A: {a1}
Example 2: Q: {q2} A: {a2}
Now answer: Q: {query}"
```

### 3. **Chain-of-Thought (CoT)**
Ask model to show reasoning steps
```
"Answer step by step:
1. First, identify the key information
2. Then, analyze the relevance
3. Finally, provide the answer"
```

### 4. **Retrieval-Augmented Generation (RAG)**
Combine retrieved context with query
```
"Use the following context to answer the question.
Context: {retrieved_docs}
Question: {query}
Answer:"
```

## 📋 Prompt Templates

### Basic RAG Prompt
```json
{
  "system": "You are a helpful assistant answering questions based on provided documents.",
  "template": "Context:\n{context}\n\nQuestion: {question}\n\nAnswer:"
}
```

### Detailed Analysis Prompt
```json
{
  "system": "You are an expert analyst. Provide detailed, structured answers.",
  "template": "Based on the following documents:\n{context}\n\nProvide a comprehensive answer to: {question}\n\nInclude:\n1. Direct answer\n2. Supporting evidence\n3. Caveats or limitations"
}
```

### Question-Answering Prompt
```json
{
  "system": "Answer questions accurately and concisely.",
  "template": "Documents:\n{context}\n\nQ: {question}\nA:"
}
```

## 🎯 Best Practices

### 1. **Clarity**
- Use clear, specific language
- Define technical terms
- Specify output format

### 2. **Structure**
- Use numbered lists
- Add section headers
- Include examples

### 3. **Context Window**
- Keep prompts concise
- Prioritize recent context
- Use summarization for long docs

### 4. **Output Format**
```
"Respond in JSON format:
{
  'answer': 'your answer here',
  'confidence': 0.95,
  'sources': ['page 1', 'page 2']
}"
```

## 📊 Prompt Engineering Techniques

| Technique | Best For | Complexity |
|-----------|----------|-----------|
| Zero-Shot | Simple queries | ⭐ |
| Few-Shot | Specific formats | ⭐⭐ |
| Chain-of-Thought | Complex reasoning | ⭐⭐⭐ |
| Self-Consistency | High accuracy | ⭐⭐⭐⭐ |
| Tree-of-Thought | Multi-step problems | ⭐⭐⭐⭐⭐ |

## 🚀 Implementation

```python
# In src/generation.py - RAGGenerator
from langchain.prompts import PromptTemplate

prompt_template = PromptTemplate(
    input_variables=["context", "question"],
    template="""Use the following context to answer the question.
Context: {context}
Question: {question}
Answer:"""
)
```

## 💡 Tips for RAG Prompts

1. **Be explicit about sources**: "Cite the document where you found this"
2. **Set expectations**: "If not found in documents, say 'Not found'"
3. **Guide structure**: "Provide answer in 2-3 sentences"
4. **Include caveats**: "State any limitations or uncertainties"

## 📝 Prompt Optimization Workflow

1. Start with simple prompt
2. Test with sample queries
3. Measure accuracy/quality
4. Iterate and refine
5. Add examples if needed
6. Optimize for speed vs quality

---

**Used in:** `src/generation.py` - RAGGenerator, `ui/app.py` - Streamlit interface
