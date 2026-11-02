# ⚠️ exception/ - Error Handling

Custom exceptions for robust error management.

## 📂 Files

- **custom_exception.py** - Exception definitions

## 🎯 Overview

**Custom Exceptions:**
- `DocumentPortalException` - Main application exception

## 🚀 Usage

```python
from exception.custom_exception import DocumentPortalException

try:
    # Some operation
    result = risky_operation()
except Exception as e:
    raise DocumentPortalException(
        "Operation failed",
        e
    ) from e
```

## 📋 Exception Handling

- Wraps original exception
- Provides context message
- Maintains exception chain
- Logs automatically

---

**Part of the RAG error handling infrastructure**
