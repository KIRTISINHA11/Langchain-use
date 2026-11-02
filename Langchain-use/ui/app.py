# -*- coding: utf-8 -*-
"""
Resume-aware ChatGPT-style Streamlit UI for Multimodal RAG with LangChain.

Behavior:
1. Select an existing project PDF OR upload a new PDF.
2. If parsed artifacts already exist on disk, load them instead of parsing again.
3. If Chroma vector store already contains the document, reuse existing index.
4. Only run missing stages.
5. Chat through LangChain RAG chain with ChatGroq LLM.

Expected location:
    <project_root>/ui/app.py
"""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import sys
from pathlib import Path
from typing import Any

import streamlit as st
from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

load_dotenv(PROJECT_ROOT / ".env")

from src.parsing import MultimodalPDFParser
from src.ingestion import DocumentIngestionPipeline
from src.generation import RAGGenerator
from src.retriever import ChromaRetriever


DATA_DIR = PROJECT_ROOT / "data"
UPLOAD_DIR = DATA_DIR / "uploads"
PARSED_ROOT = DATA_DIR / "parsed_pdf_output"
CHROMA_DIR = DATA_DIR / "chroma_vectorstore"

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
PARSED_ROOT.mkdir(parents=True, exist_ok=True)
CHROMA_DIR.mkdir(parents=True, exist_ok=True)

PARSED_JSON_FILES = (
    "page_records.json",
    "image_records.json",
    "table_records.json",
)


# =====================================================================
# Page config + CSS
# =====================================================================

st.set_page_config(
    page_title="Multimodal RAG Assistant",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
<style>
    .block-container {
        max-width: 1120px;
        padding-top: 1.6rem;
        padding-bottom: 7rem;
    }

    [data-testid="stSidebar"] {
        min-width: 330px;
        max-width: 380px;
    }

    .mmrag-title {
        font-size: 2.2rem;
        font-weight: 750;
        letter-spacing: -0.04em;
        margin-bottom: 0.15rem;
    }

    .mmrag-subtitle {
        opacity: 0.72;
        margin-bottom: 1.2rem;
    }

    .source-card {
        border: 1px solid rgba(128,128,128,.20);
        border-radius: 12px;
        padding: 10px 12px;
        margin: 6px 0;
    }

    .tiny-muted {
        opacity: 0.65;
        font-size: 0.82rem;
    }

    .ready-pill {
        display: inline-block;
        padding: 5px 10px;
        border-radius: 999px;
        border: 1px solid rgba(128,128,128,.25);
        margin-right: 6px;
        margin-bottom: 8px;
        font-size: .83rem;
    }
</style>
""",
    unsafe_allow_html=True,
)


# =====================================================================
# Session state
# =====================================================================

def init_session_state() -> None:
    defaults = {
        "document_token": None,
        "selected_pdf_path": None,
        "selected_pdf_fingerprint": None,
        "parsed_result": None,
        "parsed_pdf_path": None,
        "parsed_output_dir": None,
        "parsed_file_fingerprint": None,
        "parsed_restore_mode": None,
        "pipeline": None,
        "retriever": None,
        "rag_chain": None,
        "active_collection": None,
        "chat_messages": [],
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def reset_document_state() -> None:
    st.session_state.parsed_result = None
    st.session_state.parsed_pdf_path = None
    st.session_state.parsed_output_dir = None
    st.session_state.parsed_file_fingerprint = None
    st.session_state.parsed_restore_mode = None
    st.session_state.pipeline = None
    st.session_state.retriever = None
    st.session_state.rag_chain = None
    st.session_state.active_collection = None
    st.session_state.chat_messages = []


def clear_chat() -> None:
    st.session_state.chat_messages = []


init_session_state()


# =====================================================================
# Helper functions
# =====================================================================

def safe_filename(filename: str) -> str:
    return Path(filename).name


def file_fingerprint(file_bytes: bytes) -> str:
    return hashlib.sha256(file_bytes).hexdigest()


def fingerprint_file(path: Path) -> str:
    sha = hashlib.sha256()
    with path.open("rb") as file:
        for block in iter(lambda: file.read(1024 * 1024), b""):
            sha.update(block)
    return sha.hexdigest()


def deepest_error_message(exc: BaseException) -> str:
    current: BaseException = exc
    visited: set[int] = set()
    
    while current.__cause__ is not None and id(current) not in visited:
        visited.add(id(current))
        current = current.__cause__
    
    return f"{type(current).__name__}: {current}"


def current_filename() -> str | None:
    path = st.session_state.selected_pdf_path
    if not path:
        return None
    return Path(path).name


def is_chat_ready() -> bool:
    return bool(
        st.session_state.parsed_result
        and st.session_state.rag_chain
    )


def discover_project_pdfs() -> list[Path]:
    discovered: dict[str, Path] = {}
    
    for folder in (DATA_DIR, UPLOAD_DIR):
        if not folder.exists():
            continue
        for path in folder.glob("*.pdf"):
            try:
                key = str(path.resolve()).lower()
            except OSError:
                key = str(path).lower()
            discovered[key] = path
    
    return sorted(discovered.values(), key=lambda path: path.name.lower())


def parsed_artifacts_complete(output_dir: Path) -> bool:
    return all((output_dir / filename).exists() for filename in PARSED_JSON_FILES)


def load_existing_parsed_result(
    pdf_path: Path,
    output_dir: Path,
) -> dict[str, Any]:
    with (output_dir / "page_records.json").open("r", encoding="utf-8") as file:
        pages = json.load(file)
    
    with (output_dir / "image_records.json").open("r", encoding="utf-8") as file:
        images = json.load(file)
    
    with (output_dir / "table_records.json").open("r", encoding="utf-8") as file:
        tables = json.load(file)
    
    parser = MultimodalPDFParser(
        pdf_path=str(pdf_path),
        output_dir=str(output_dir),
    )
    
    parser.page_records = pages
    parser.image_records = images
    parser.table_records = tables
    
    documents = parser.create_langchain_documents()
    
    return {
        "pages": pages,
        "images": images,
        "tables": tables,
        "documents": documents,
        "output_dir": str(output_dir),
    }


def find_existing_parsed_output(
    pdf_path: Path,
    fingerprint: str,
) -> tuple[Path | None, str | None]:
    candidates = [
        PARSED_ROOT / pdf_path.stem,
        PARSED_ROOT,
    ]
    
    for output_dir in candidates:
        if not parsed_artifacts_complete(output_dir):
            continue
        return output_dir, "existing"
    
    return None, None


def try_restore_parsed_state(
    pdf_path: Path,
    fingerprint: str,
) -> bool:
    output_dir, mode = find_existing_parsed_output(pdf_path, fingerprint)
    
    if output_dir is None:
        return False
    
    try:
        parsed = load_existing_parsed_result(pdf_path, output_dir)
        st.session_state.parsed_result = parsed
        st.session_state.parsed_pdf_path = str(pdf_path)
        st.session_state.parsed_output_dir = str(output_dir)
        st.session_state.parsed_file_fingerprint = fingerprint
        st.session_state.parsed_restore_mode = mode
        return True
    except Exception:
        return False


# =====================================================================
# Rendering helpers
# =====================================================================

def render_pipeline_badges() -> None:
    parsed = st.session_state.parsed_result is not None
    indexed = st.session_state.rag_chain is not None
    ready = is_chat_ready()
    
    st.markdown(
        (
            f'<span class="ready-pill">'
            f'{"✅" if parsed else "○"} Parsed'
            f'</span>'
            f'<span class="ready-pill">'
            f'{"✅" if indexed else "○"} Indexed'
            f'</span>'
            f'<span class="ready-pill">'
            f'{"✅" if ready else "○"} Chat ready'
            f'</span>'
        ),
        unsafe_allow_html=True,
    )


def render_parse_summary(parsed: dict[str, Any]) -> None:
    col1, col2, col3, col4 = st.columns(4)
    
    col1.metric("Pages", len(parsed.get("pages", [])))
    col2.metric("Tables", len(parsed.get("tables", [])))
    col3.metric("Images", len(parsed.get("images", [])))
    col4.metric("Documents", len(parsed.get("documents", [])))


def render_document_inspector(parsed: dict[str, Any]) -> None:
    with st.expander("🔎 Document inspector", expanded=False):
        text_tab, table_tab, image_tab = st.tabs(["Text", "Tables", "Images"])
        
        with text_tab:
            page_documents = [
                doc for doc in parsed.get("documents", [])
                if doc.metadata.get("content_type") == "page_text"
            ]
            
            if not page_documents:
                st.info("No page text documents found.")
            else:
                page_options = [
                    int(doc.metadata.get("page_number", i + 1))
                    for i, doc in enumerate(page_documents)
                ]
                
                selected_page = st.selectbox(
                    "Preview page",
                    options=page_options,
                    key="preview_page",
                )
                
                selected_doc = next(
                    (doc for doc in page_documents
                     if int(doc.metadata.get("page_number", -1)) == selected_page),
                    None,
                )
                
                if selected_doc:
                    st.text(selected_doc.page_content[:12000])
        
        with table_tab:
            tables = parsed.get("tables", [])
            
            if not tables:
                st.info("No tables detected.")
            else:
                labels = [
                    f"Page {t.get('page_number', '?')} · Table {t.get('table_index', '?')}"
                    for t in tables
                ]
                
                index = st.selectbox("Preview table", range(len(tables)), 
                                    format_func=lambda i: labels[i], key="preview_table")
                
                table = tables[index]
                if table.get("markdown"):
                    st.markdown(table["markdown"])
                else:
                    st.write(table.get("raw_table"))
        
        with image_tab:
            images = parsed.get("images", [])
            
            if not images:
                st.info("No embedded images detected.")
            else:
                labels = [
                    f"Page {img.get('page_number', '?')} · Image {img.get('image_index', '?')}"
                    for img in images
                ]
                
                index = st.selectbox("Preview image", range(len(images)),
                                    format_func=lambda i: labels[i], key="preview_image")
                
                image_record = images[index]
                image_path = Path(str(image_record.get("image_path", "")))
                
                if image_path.exists():
                    st.image(str(image_path), caption=labels[index], width="stretch")
                else:
                    st.warning(f"Image file not found: {image_path}")


def render_source_cards(sources: list[dict[str, Any]]) -> None:
    if not sources:
        return
    
    with st.expander(f"Sources · {len(sources)} retrieved", expanded=False):
        for source in sources:
            citation = source.get("citation", "Unknown source")
            content_type = source.get("content_type", "unknown")
            
            st.markdown(
                f"""
<div class="source-card">
    <strong>{citation}</strong><br/>
    <span class="tiny-muted">type: {content_type}</span>
</div>
""",
                unsafe_allow_html=True,
            )


def render_chat_history() -> None:
    for message in st.session_state.chat_messages:
        role = message.get("role", "assistant")
        avatar = "🧑‍💻" if role == "user" else "🧠"
        
        with st.chat_message(role, avatar=avatar):
            if role == "assistant":
                st.markdown(message.get("content", ""))
                render_source_cards(message.get("sources", []))
            else:
                st.markdown(message.get("content", ""))


# =====================================================================
# Sidebar: Document selection
# =====================================================================

st.sidebar.markdown("## 🧠 Multimodal RAG")
st.sidebar.caption("Resume-aware document workspace")

existing_pdfs = discover_project_pdfs()
source_options = ["Upload new PDF"]

if existing_pdfs:
    source_options.insert(0, "Use existing project PDF")

source_mode = st.sidebar.radio("Document source", options=source_options)

selected_pdf_path: Path | None = None
selected_fingerprint: str | None = None

if source_mode == "Use existing project PDF":
    selected_index = st.sidebar.selectbox(
        "Existing PDF",
        options=range(len(existing_pdfs)),
        format_func=lambda i: existing_pdfs[i].name,
    )
    
    selected_pdf_path = existing_pdfs[selected_index]
    
    try:
        selected_fingerprint = fingerprint_file(selected_pdf_path)
    except Exception as exc:
        st.sidebar.error(deepest_error_message(exc))

else:
    uploaded_file = st.sidebar.file_uploader(
        "Upload a PDF",
        type=["pdf"],
        accept_multiple_files=False,
        key="pdf_uploader",
    )
    
    if uploaded_file is not None:
        uploaded_bytes = uploaded_file.getvalue()
        filename = safe_filename(uploaded_file.name)
        selected_fingerprint = file_fingerprint(uploaded_bytes)
        selected_pdf_path = UPLOAD_DIR / filename
        
        if (not selected_pdf_path.exists() or 
            fingerprint_file(selected_pdf_path) != selected_fingerprint):
            selected_pdf_path.write_bytes(uploaded_bytes)
        
        st.sidebar.caption(f"{filename} · {len(uploaded_bytes) / (1024 * 1024):.2f} MB")


# =====================================================================
# Document changed -> restore or parse
# =====================================================================

if selected_pdf_path is not None and selected_fingerprint is not None:
    document_token = f"{selected_pdf_path.resolve()}|{selected_fingerprint}"
    
    if st.session_state.document_token != document_token:
        reset_document_state()
        
        st.session_state.document_token = document_token
        st.session_state.selected_pdf_path = str(selected_pdf_path)
        st.session_state.selected_pdf_fingerprint = selected_fingerprint
        
        try:
            try_restore_parsed_state(
                pdf_path=selected_pdf_path,
                fingerprint=selected_fingerprint,
            )
        except Exception as exc:
            st.sidebar.warning("Saved parsed artifacts could not be loaded.")
            st.sidebar.code(deepest_error_message(exc))
    
    else:
        st.session_state.selected_pdf_path = str(selected_pdf_path)
        st.session_state.selected_pdf_fingerprint = selected_fingerprint

else:
    if st.session_state.document_token is not None:
        st.session_state.document_token = None
        reset_document_state()


# =====================================================================
# Sidebar: Parsing
# =====================================================================

if selected_pdf_path is not None:
    st.sidebar.markdown("---")
    st.sidebar.markdown("#### Document pipeline")
    
    if st.session_state.parsed_result is not None:
        if st.session_state.parsed_restore_mode is not None:
            st.sidebar.success("1 · Existing parsed data loaded")
            st.sidebar.caption("No re-parsing.")
        else:
            st.sidebar.success("1 · PDF parsed")
        
        force_parse = st.sidebar.button("Re-parse PDF", use_container_width=True)
    else:
        force_parse = st.sidebar.button(
            "1 · Parse PDF",
            type="primary",
            use_container_width=True,
        )
    
    if force_parse:
        try:
            output_dir = PARSED_ROOT / selected_pdf_path.stem
            
            if output_dir.exists():
                shutil.rmtree(output_dir)
            
            output_dir.mkdir(parents=True, exist_ok=True)
            
            with st.status("Parsing PDF...", expanded=True) as status:
                parser = MultimodalPDFParser(
                    pdf_path=str(selected_pdf_path),
                    output_dir=str(output_dir),
                    render_scale=2.0,
                )
                
                parsed = parser.parse(save_output=True)
                
                st.session_state.parsed_result = parsed
                st.session_state.parsed_pdf_path = str(selected_pdf_path)
                st.session_state.parsed_output_dir = str(output_dir)
                st.session_state.parsed_file_fingerprint = selected_fingerprint
                st.session_state.parsed_restore_mode = None
                st.session_state.rag_chain = None
                st.session_state.chat_messages = []
                
                status.update(label="PDF parsed", state="complete", expanded=False)
            
            st.rerun()
        
        except Exception as exc:
            st.sidebar.error("PDF parsing failed.")
            st.sidebar.code(deepest_error_message(exc))


# =====================================================================
# Sidebar: Ingestion to Chroma
# =====================================================================

collection_name = st.sidebar.text_input(
    "Collection name",
    value="pdf_documents",
    key="collection_name_input",
).strip() if selected_pdf_path is not None else None

if (selected_pdf_path is not None and 
    st.session_state.parsed_result is not None):
    
    if st.session_state.rag_chain is not None:
        st.sidebar.success("2 · Indexed in Chroma")
        
        if st.sidebar.button("Re-index document", use_container_width=True):
            st.session_state.rag_chain = None
            st.session_state.pipeline = None
            st.session_state.chat_messages = []
            st.rerun()
    
    else:
        with st.sidebar.expander("Advanced indexing", expanded=False):
            chunk_size = st.number_input(
                "Chunk size",
                min_value=200,
                max_value=10000,
                value=1000,
                step=100,
                key="chunk_size_input",
            )
            
            chunk_overlap = st.number_input(
                "Chunk overlap",
                min_value=0,
                max_value=2000,
                value=200,
                step=20,
                key="chunk_overlap_input",
            )
        
        invalid_chunking = chunk_overlap >= chunk_size
        
        if invalid_chunking:
            st.sidebar.error("Chunk overlap must be smaller than chunk size.")
        
        if st.sidebar.button(
            "2 · Ingest to Chroma",
            type="primary",
            use_container_width=True,
            disabled=(invalid_chunking or not collection_name),
        ):
            try:
                documents = st.session_state.parsed_result["documents"]
                
                with st.status("Indexing document...", expanded=True) as status:
                    pipeline = DocumentIngestionPipeline(
                        chroma_persist_dir=str(CHROMA_DIR),
                        embedding_model="all-MiniLM-L6-v2",
                        chunk_size=int(chunk_size),
                        chunk_overlap=int(chunk_overlap),
                        groq_model="openai/gpt-oss-20b",
                        groq_temperature=0.0,
                    )
                    
                    pipeline.ingest_documents(
                        documents=documents,
                        collection_name=collection_name,
                        split_documents=True,
                    )

                    # Initialize RAG generator
                    generator = RAGGenerator(
                        chroma_persist_dir=str(CHROMA_DIR),
                        collection_name=collection_name,
                        groq_model="openai/gpt-oss-20b",
                        groq_temperature=0.0,
                    )

                    st.session_state.rag_chain = generator
                    st.session_state.pipeline = pipeline
                    st.session_state.active_collection = collection_name
                    st.session_state.chat_messages = []
                    
                    status.update(label="Indexing complete", state="complete", expanded=False)
                
                st.rerun()
            
            except Exception as exc:
                st.sidebar.error("Chroma ingestion failed.")
                st.sidebar.code(deepest_error_message(exc))


# =====================================================================
# Sidebar: Chat settings
# =====================================================================

if is_chat_ready():
    st.sidebar.markdown("---")
    st.sidebar.markdown("#### Chat settings")
    
    top_k = st.sidebar.slider(
        "Top-K retrieval",
        min_value=2,
        max_value=15,
        value=4,
        key="top_k_input",
    )
    
    if st.sidebar.button("Clear chat", use_container_width=True):
        clear_chat()
        st.rerun()


# =====================================================================
# Sidebar: Document workspace
# =====================================================================

st.sidebar.markdown("---")
st.sidebar.markdown("#### Document status")

with st.sidebar:
    render_pipeline_badges()

if selected_pdf_path:
    st.sidebar.caption(selected_pdf_path.name)
    
    if st.session_state.parsed_result:
        with st.sidebar.expander("📄 Document details", expanded=False):
            render_parse_summary(st.session_state.parsed_result)
        
        with st.sidebar:
            render_document_inspector(st.session_state.parsed_result)


# =====================================================================
# Main content
# =====================================================================

st.markdown(
    '<div class="mmrag-title">Multimodal Document Assistant</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="mmrag-subtitle">Ask questions about text, tables, and visual content in your documents.</div>',
    unsafe_allow_html=True,
)


# =====================================================================
# Chat readiness checks
# =====================================================================

if selected_pdf_path is None:
    st.markdown("### Start a document conversation")
    st.caption("Choose an existing PDF or upload a new one from the sidebar.")
    st.stop()

if st.session_state.parsed_result is None:
    st.markdown("### Preparing your document")
    st.caption("No parsed artifacts found. Use **Parse PDF** in the sidebar.")
    st.stop()

if st.session_state.rag_chain is None:
    st.markdown("### Almost ready")
    st.caption("Use **Ingest to Chroma** in the sidebar to enable document chat.")
    st.stop()


# =====================================================================
# Chat interface
# =====================================================================

if not st.session_state.chat_messages:
    st.markdown("### What would you like to know?")
    st.caption("Ask about content, tables, or visual elements in the document.")

render_chat_history()

typed_prompt = st.chat_input("Ask anything about the document...", key="document_chat_input")

if typed_prompt:
    user_message = {"role": "user", "content": str(typed_prompt)}
    st.session_state.chat_messages.append(user_message)
    
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(str(typed_prompt))
    
    with st.chat_message("assistant", avatar="🧠"):
        try:
            with st.status("Searching document...", expanded=False) as status:
                # Generate answer using RAGGenerator
                result = st.session_state.rag_chain.generate_answer(
                    query=str(typed_prompt),
                    k=4
                )

                answer = result["answer"]
                retrieved_docs = result["retrieved_docs"]

                status.update(label="Answer ready", state="complete", expanded=False)

            assistant_message = {
                "role": "assistant",
                "content": answer,
                "sources": [
                    {
                        "citation": f"Page {doc.metadata.get('page_number', '?')}",
                        "content_type": doc.metadata.get("content_type", "text"),
                    }
                    for doc in retrieved_docs
                ],
            }

            st.session_state.chat_messages.append(assistant_message)

            st.markdown(assistant_message["content"])
            render_source_cards(assistant_message["sources"])
        
        except Exception as exc:
            error_text = deepest_error_message(exc)
            st.error("Could not generate an answer.")
            st.code(error_text)
            
            st.session_state.chat_messages.append({
                "role": "assistant",
                "content": f"Error: {error_text}",
                "sources": [],
            })
