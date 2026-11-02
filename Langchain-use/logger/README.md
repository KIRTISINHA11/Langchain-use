# 📝 logger/ - Structured Logging System

Production-grade logging with structured output and file persistence.

## 📂 Files

- **custom_logger.py** - Main logger implementation

## 🎯 Overview

**Features:**
- Structured logging (JSON format)
- File-based persistence
- Timestamp tracking
- Event categorization
- Exception logging
- Fallback to standard logging

## 🚀 Usage

```python
from logger.custom_logger import CustomLogger

# Initialize
logger = CustomLogger().get_logger(__name__)

# Log events
logger.info("document_parsed", pages=10, duration=2.5)
logger.debug("chunk_created", size=1000, overlap=200)
logger.warning("token_limit_approaching", tokens=7500, max=8000)
logger.error("parsing_failed", error="PDF corrupted")
logger.exception("unexpected_error", traceback="...")
```

## 📋 Log Format

```json
{
  "timestamp": "2026-11-02T05:25:51.367952Z",
  "level": "info",
  "event": "document_parsed",
  "pages": 10,
  "duration": 2.5
}
```

## 🗂️ Log Files

Logs stored in:
```
logs/
├── 11_02_2026_05_25_51.log
├── 11_02_2026_06_30_12.log
└── ...
```

---

**Part of the RAG logging infrastructure**
