# 🖼️ Multimodal PDF Parsing for RAG

Complete PDF parsing pipeline that extracts **text, tables, and images** for integration with Vision LLMs.

---

## 📁 **Output Structure**

```
data/parsed_pdf_output/
├── extracted_images/           ← 🖼️ Embedded images from PDF
│   ├── page_001_image_1.png
│   ├── page_001_image_2.jpg
│   └── ...
│
├── page_images/                ← 📄 Full-page rendered images
│   ├── page_001.png
│   ├── page_002.png
│   └── ...
│
├── page_records.json           ← Text + metadata
├── image_records.json          ← Image references
├── table_records.json          ← Table content
├── rag_ready_documents.md      ← All LangChain docs
└── extracted_tables.md         ← Tables in markdown
```

---

## 🚀 **Quick Start**

### **1. Parse PDF (Extract All Content)**

```python
from pathlib import Path
from src.data_parsing import MultimodalPDFParser

DATA_DIR = Path(r"C:\Users\Admin\Agentic AI Projects\AI\RAG\Langchain-use\data")
PDF_PATH = DATA_DIR / "Client_Contracts_Policies_and_Incident_Records.pdf"
OUTPUT_DIR = DATA_DIR / "parsed_pdf_output"

# Initialize parser
parser = MultimodalPDFParser(
    pdf_path=str(PDF_PATH),
    output_dir=str(OUTPUT_DIR),
    render_scale=2.0  # Higher = better quality (slower)
)

# Parse and extract everything
result = parser.parse(save_output=True)

# Access results
documents = result["documents"]        # LangChain docs
page_images = result["page_image_dir"] # Full page renders
embedded_images = result["image_dir"]  # Extracted images
```

### **2. Use Images with Vision LLM**

```python
from src.vision_rag import VisionRAGIntegration

# Get image path
image_path = "page_images/page_001.png"

# Create Claude Vision message
message = VisionRAGIntegration.create_claude_vision_message(
    image_path=image_path,
    query="What is the main content of this page?"
)

# Send to Claude
response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    messages=[message]
)

print(response.content[0].text)
```

---

## 📊 **Document Types Created**

| Type | Source | For Vision LLM? | Example Use |
|------|--------|---|---|
| **page_text** | PyMuPDF text extraction | ❌ | Dense retrieval, semantic search |
| **page_image** | PyMuPDF page render | ✅ | "Describe this page layout" |
| **embedded_image** | Extracted from PDF | ✅ | "What does this diagram show?" |
| **table** | pdfplumber extraction | ❌ | "Find data about X in tables" |

---

## 🧠 **Vision LLM Integration Examples**

### **Claude Vision (Recommended)**

```python
import anthropic

client = anthropic.Anthropic()

image_path = "page_images/page_001.png"

message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/png",
                        "data": VisionRAGIntegration.encode_image_to_base64(image_path),
                    },
                },
                {
                    "type": "text",
                    "text": "Extract all text and important information from this page"
                }
            ],
        }
    ],
)

print(message.content[0].text)
```

### **GPT-4V (OpenAI)**

```python
from openai import OpenAI

client = OpenAI()

image_path = "page_images/page_001.png"

message = VisionRAGIntegration.create_gpt4v_vision_message(
    image_path=image_path,
    query="Extract all text and important information from this page"
)

response = client.chat.completions.create(
    model="gpt-4-vision-preview",
    messages=[message],
    max_tokens=1024
)

print(response.choices[0].message.content)
```

### **Gemini Vision (Google)**

```python
import google.generativeai as genai

genai.configure(api_key="YOUR_GEMINI_API_KEY")

image_path = "page_images/page_001.png"

message = VisionRAGIntegration.create_gemini_vision_message(
    image_path=image_path,
    query="Extract all text and important information from this page"
)

response = genai.GenerativeModel('gemini-1.5-pro').generate_content([message])

print(response.text)
```

---

## 🔄 **Complete RAG Pipeline with Vision LLM**

```python
from pathlib import Path
from src.data_parsing import MultimodalPDFParser
from src.vision_rag import VisionRAGIntegration
import anthropic

# Step 1: Parse PDF
parser = MultimodalPDFParser(
    pdf_path="pdf_file.pdf",
    output_dir="output_dir"
)
result = parser.parse(save_output=True)
documents = result["documents"]

# Step 2: Separate vision documents
vision_docs = [
    doc for doc in documents 
    if doc.metadata.get("content_type") in ["page_image", "embedded_image"]
]

# Step 3: User query
user_query = "What are the contract terms mentioned?"

# Step 4: Retrieve relevant images
relevant_images = [doc.metadata["image_path"] for doc in vision_docs[:3]]

# Step 5: Send to Vision LLM
client = anthropic.Anthropic()
messages = []

for image_path in relevant_images:
    msg = VisionRAGIntegration.create_claude_vision_message(
        image_path=image_path,
        query=user_query
    )
    messages.append(msg)

# Step 6: Get response
response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=2048,
    messages=messages
)

print("Vision LLM Response:")
print(response.content[0].text)
```

---

## 📸 **What Gets Extracted**

### **1. Full Page Images** 📄
- Complete rendered page
- Shows layout, formatting, images, tables
- Perfect for visual context
- Render scale: 2.0x = higher quality

### **2. Embedded Images** 🖼️
- Diagrams, charts, photos
- Extracted directly from PDF
- Preserved in original format

### **3. Text Content** 📝
- Selectable text from pages
- Used for semantic search
- Indexed in vector store

### **4. Tables** 📊
- Extracted to markdown/CSV
- Searchable by content
- Preserved structure

---

## ⚙️ **Configuration**

### **Parse Scale (Quality vs Speed)**

```python
# Faster (lower quality)
parser = MultimodalPDFParser(pdf_path="...", output_dir="...", render_scale=1.0)

# Balanced (recommended)
parser = MultimodalPDFParser(pdf_path="...", output_dir="...", render_scale=2.0)

# High quality (slower)
parser = MultimodalPDFParser(pdf_path="...", output_dir="...", render_scale=3.0)
```

### **Data Paths**

```python
DATA_DIR = Path(r"C:\Users\Admin\Agentic AI Projects\AI\RAG\Langchain-use\data")
PDF_PATH = DATA_DIR / "Client_Contracts_Policies_and_Incident_Records.pdf"
OUTPUT_DIR = DATA_DIR / "parsed_pdf_output"
```

---

## 🎯 **Best Practices**

✅ **DO:**
- Use page images for visual context
- Use tables for structured data extraction
- Use text for semantic search
- Cache vision LLM responses (expensive!)
- Process images in batches

❌ **DON'T:**
- Send every page image to LLM (expensive)
- Ignore text extraction (slower than text)
- Mix vision and text in same query without reason
- Forget to handle API rate limits

---

## 💾 **Dependencies**

```txt
pymupdf>=1.23.8          # PDF text/image extraction
pdfplumber>=0.10.3       # Table extraction
pandas>=2.0.0            # Table processing
pillow>=10.0.0           # Image handling
langchain-core>=0.1.0    # Document conversion
anthropic>=0.7.0         # Claude Vision API (optional)
openai>=1.0.0            # GPT-4V API (optional)
google-generativeai>=0.3.0  # Gemini API (optional)
```

Install:
```bash
pip install pymupdf pdfplumber pandas pillow langchain-core
```

---

## 📊 **Output Summary**

After parsing:
```
✅ Pages:           10
✅ Embedded Images: 5
✅ Tables:          3
✅ Documents:       18 (text + images + tables)

📂 Directories:
   - extracted_images/  (5 images)
   - page_images/       (10 pages)
   - JSON records
   - Markdown exports
```

---

## 🔗 **Next Steps**

1. **Parse PDF** → `MultimodalPDFParser.parse()`
2. **Filter images** → Get `page_image`, `embedded_image` docs
3. **Query Vision LLM** → Use `VisionRAGIntegration` helpers
4. **Combine with vector DB** → Hybrid semantic + vision search
5. **Build RAG chain** → LangChain + Vision LLM + Vector DB

---

## 🆘 **Troubleshooting**

**Q: Images not being extracted?**
- Check PDF has embedded images
- Verify output directories created
- Check file permissions

**Q: Vision LLM API errors?**
- Verify API keys
- Check image path validity
- Monitor rate limits
- Use base64 encoding correctly

**Q: Slow parsing?**
- Reduce `render_scale` (1.0 instead of 2.0)
- Skip full page images if not needed
- Process large PDFs in chunks

---

## 📚 **Resources**

- [PyMuPDF Documentation](https://pymupdf.readthedocs.io/)
- [pdfplumber Documentation](https://github.com/jsvine/pdfplumber)
- [Claude Vision API](https://docs.anthropic.com/en/api/vision)
- [GPT-4V Documentation](https://platform.openai.com/docs/guides/vision)
- [Gemini Vision](https://ai.google.dev/tutorials/python_quickstart)

---

**Ready to build multimodal RAG? 🚀**
