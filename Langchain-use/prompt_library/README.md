# 💬 prompt_library/ - LLM Prompts

Centralized prompt management for consistent LLM behavior.

## 📂 Files

- **prompt.py** - All system and user prompts

## 🎯 Overview

**Prompts Included:**
- System prompts for RAG context
- User prompt templates
- Suggested prompts for users
- Multimodal RAG prompts

## 🚀 Usage

```python
from prompt_library.prompt import (
    MULTIMODAL_RAG_SYSTEM_PROMPT,
    CHAT_SUGGESTED_PROMPTS
)

# Use system prompt
system_msg = MULTIMODAL_RAG_SYSTEM_PROMPT

# Show suggestions to users
suggestions = CHAT_SUGGESTED_PROMPTS
```

## 📝 Prompt Examples

```
System: "You are an intelligent assistant that answers questions based on provided documents..."

User: "What are the contract terms mentioned in the documents?"

Suggestions:
- "What policies are covered?"
- "Summarize the key points"
- "What are the incident records?"
```

---

**Part of the RAG prompt engineering system**
