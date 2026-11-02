# 🔍 Data Parsing - PDF & Document Extraction

End-to-end guide for extracting text, images, and tables from PDFs using multiple parsing strategies.

## 📂 Contents

### Part 1: LangChain Data Loaders
- **data_parsing_part1_langchain_data_loaders.ipynb**
- LangChain's built-in document loaders
- PyPDFLoader, PDFPlumberLoader, and others
- Best for: Integration with LangChain pipeline

### Part 2: PyMuPDF & PDFPlumber
- **data_parsing_part2_pymupdf_pdfplumber.ipynb**
- Direct PDF parsing with fitz (PyMuPDF)
- PDFPlumber for table extraction
- Best for: Detailed control over parsing

### Part 3: Docling
- **data_parsing_part3_docling.ipynb**
- Microsoft's advanced document parser
- Converts PDFs to structured markdown
- Best for: Complex document layouts

### Part 4: LlamaParser
- **data_parsing_part4_llama_parser.ipynb**
- LLM-powered parsing
- Understands complex layouts
- Best for: Scanned documents, complex formatting

## 🛠️ Parsing Strategies Comparison

| Tool | Speed | Accuracy | Tables | Images | Cost |
|------|-------|----------|--------|--------|------|
| PyPDFLoader | ⚡⚡⚡ | ⭐⭐ | ❌ | ❌ | Free |
| PyMuPDF | ⚡⚡ | ⭐⭐⭐ | ⭐⭐ | ✅ | Free |
| PDFPlumber | ⚡⭐ | ⭐⭐⭐⭐ | ✅ | ⭐ | Free |
| Docling | ⭐⭐ | ⭐⭐⭐⭐⭐ | ✅ | ✅ | Free |
| LlamaParser | ⭐ | ⭐⭐⭐⭐⭐ | ✅ | ✅ | Paid |

## 📦 Output Structure

```json
{
  "text_content": {
    "page_1": "Full text from page 1...",
    "page_2": "Full text from page 2..."
  },
  "images": {
    "page_1_image_1": "base64_image_data",
    "page_2_image_1": "base64_image_data"
  },
  "tables": {
    "page_1_table_1": "Markdown formatted table"
  }
}
```

## 🚀 Quick Start

### PyMuPDF (Fastest)
```python
import fitz

doc = fitz.open("document.pdf")
for page in doc:
    text = page.get_text()
    images = page.get_images()
```

### PDFPlumber (Best for Tables)
```python
import pdfplumber

with pdfplumber.open("document.pdf") as pdf:
    for page in pdf.pages:
        tables = page.extract_tables()
```

### Docling (Most Accurate)
```python
from docling.document_converter import DocumentConverter

converter = DocumentConverter()
result = converter.convert("document.pdf")
markdown = result.document.export_to_markdown()
```

## 📊 Use Cases

| Use Case | Recommended Tool |
|----------|------------------|
| Simple text extraction | PyMuPDFLoader |
| Extract tables | PDFPlumber |
| Images + text | PyMuPDF |
| Complex layouts | Docling |
| Scanned documents | LlamaParser |

## 🔗 Integration

```python
# In src/data_parsing.py
from src.data_parsing import MultimodalPDFParser

parser = MultimodalPDFParser()
documents = parser.parse_pdf("input.pdf")
# Output: [Document(page_content="...", metadata={...})]
```

---

**Integrated in:** `src/data_parsing.py` - MultimodalPDFParser
