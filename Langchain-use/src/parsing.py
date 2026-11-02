# -*- coding: utf-8 -*-
"""
data_parsing.py

Multimodal PDF parsing pipeline for RAG.
Extracts text, images, tables, and creates vision-compatible documents.

Supports:
1. PyMuPDF      -> selectable text, page rendering, embedded images
2. pdfplumber   -> table extraction
3. LangChain    -> Document conversion
4. Vision LLM   -> Can process images directly in RAG
"""

import json
import sys
from pathlib import Path
from typing import Any, Dict, List

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import pandas as pd
from PIL import Image
from langchain_core.documents import Document

# Import custom logger and exception
from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException

# Initialize logger
logger = CustomLogger().get_logger(__name__)


class MultimodalPDFParser:
    """
    Parse PDF containing:
    - selectable text
    - tables
    - embedded images
    - full page renders
    - page metadata

    Outputs are vision-compatible for multimodal LLM integration.
    Perfect for feeding images directly to Claude, GPT-4V, or other vision LLMs.
    """

    def __init__(
        self,
        pdf_path: str,
        output_dir: str,
        render_scale: float = 2.0,
    ):
        self.pdf_path = Path(pdf_path)
        self.output_dir = Path(output_dir)
        self.image_dir = self.output_dir / "extracted_images"
        self.page_image_dir = self.output_dir / "page_images"
        self.render_scale = render_scale

        self.page_records: List[Dict[str, Any]] = []
        self.image_records: List[Dict[str, Any]] = []
        self.table_records: List[Dict[str, Any]] = []
        self.langchain_docs: List[Document] = []

        try:
            self._validate_pdf()
            self._create_output_directories()
            logger.info(
                "multimodal_pdf_parser_initialized",
                pdf_path=str(self.pdf_path),
                output_dir=str(self.output_dir),
                render_scale=self.render_scale,
            )
        except FileNotFoundError as exc:
            logger.exception(
                "pdf_validation_failed",
                pdf_path=str(self.pdf_path),
                error=str(exc),
            )
            raise DocumentPortalException(
                f"PDF file not found: {self.pdf_path}",
                exc,
            ) from exc
        except Exception as exc:
            logger.exception(
                "pdf_parser_initialization_failed",
                pdf_path=str(self.pdf_path),
                error=str(exc),
            )
            raise DocumentPortalException(
                "Failed to initialize the PDF parser",
                exc,
            ) from exc

    # ============================================================
    # Setup
    # ============================================================

    def _validate_pdf(self) -> None:
        """Validate that the input PDF exists."""
        if not self.pdf_path.exists():
            raise FileNotFoundError(f"PDF file not found: {self.pdf_path}")
        logger.debug(
            "pdf_validation_successful",
            pdf_path=str(self.pdf_path),
        )

    def _create_output_directories(self) -> None:
        """Create all necessary output directories."""
        try:
            self.output_dir.mkdir(parents=True, exist_ok=True)
            self.image_dir.mkdir(parents=True, exist_ok=True)
            self.page_image_dir.mkdir(parents=True, exist_ok=True)

            logger.info(
                "output_directories_created",
                output_dir=str(self.output_dir),
                image_dir=str(self.image_dir),
                page_image_dir=str(self.page_image_dir),
            )
        except Exception as exc:
            logger.exception(
                "directory_creation_failed",
                error=str(exc),
            )
            raise DocumentPortalException(
                "Failed to create output directories",
                exc,
            ) from exc

    # ============================================================
    # PyMuPDF: Text + Images + Page Rendering
    # ============================================================

    def extract_text_and_images(self) -> tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        """
        Extract:
        - selectable page text
        - page dimensions
        - full-page rendered images
        - embedded images

        Returns:
            (page_records, image_records)
        """
        import pymupdf as fitz

        page_records: List[Dict[str, Any]] = []
        image_records: List[Dict[str, Any]] = []

        pdf = None
        try:
            pdf = fitz.open(str(self.pdf_path))
            logger.info(
                "pdf_opened_successfully",
                pdf_path=str(self.pdf_path),
                total_pages=len(pdf),
            )

            for page_index in range(len(pdf)):
                try:
                    page = pdf[page_index]
                    page_number = page_index + 1

                    # Get embedded images in page
                    images = page.get_images(full=True)

                    # Extract selectable text
                    selectable_text = page.get_text("text").strip()

                    # Render full page as image
                    logger.debug(
                        "rendering_page_to_image",
                        page_number=page_number,
                        render_scale=self.render_scale,
                    )

                    pixmap = page.get_pixmap(
                        matrix=fitz.Matrix(self.render_scale, self.render_scale)
                    )
                    page_image_path = (
                        self.page_image_dir / f"page_{page_number:03d}.png"
                    )
                    pixmap.save(str(page_image_path))

                    page_info = {
                        "page_number": page_number,
                        "text": selectable_text,
                        "embedded_image_count": len(images),
                        "width": page.rect.width,
                        "height": page.rect.height,
                        "character_count": len(selectable_text),
                        "page_image_path": str(page_image_path),
                    }

                    page_records.append(page_info)

                    logger.info(
                        "page_extracted",
                        page_number=page_number,
                        character_count=len(selectable_text),
                        embedded_images=len(images),
                        page_image_path=str(page_image_path),
                    )

                    # Extract embedded images
                    for image_index, image_info in enumerate(images, start=1):
                        try:
                            xref = image_info[0]
                            base_image = pdf.extract_image(xref)

                            image_bytes = base_image["image"]
                            image_ext = base_image["ext"]

                            image_path = (
                                self.image_dir
                                / f"page_{page_number:03d}_image_{image_index}.{image_ext}"
                            )

                            with open(image_path, "wb") as file:
                                file.write(image_bytes)

                            image_records.append(
                                {
                                    "page_number": page_number,
                                    "image_index": image_index,
                                    "image_path": str(image_path),
                                    "image_ext": image_ext,
                                    "image_size_bytes": len(image_bytes),
                                }
                            )

                            logger.debug(
                                "embedded_image_extracted",
                                page_number=page_number,
                                image_index=image_index,
                                image_path=str(image_path),
                                image_size_bytes=len(image_bytes),
                            )
                        except Exception as exc:
                            logger.warning(
                                "embedded_image_extraction_failed",
                                page_number=page_number,
                                image_index=image_index,
                                error=str(exc),
                            )
                            # Continue processing other images

                except Exception as exc:
                    logger.warning(
                        "page_extraction_failed",
                        page_number=page_index + 1,
                        error=str(exc),
                    )
                    # Continue processing other pages

        except Exception as exc:
            logger.exception(
                "text_and_image_extraction_failed",
                pdf_path=str(self.pdf_path),
                error=str(exc),
            )
            raise DocumentPortalException(
                f"Failed to extract text and images from {self.pdf_path}",
                exc,
            ) from exc
        finally:
            if pdf:
                pdf.close()
                logger.debug("pdf_closed")

        self.page_records = page_records
        self.image_records = image_records

        logger.info(
            "text_and_image_extraction_completed",
            total_pages=len(page_records),
            total_embedded_images=len(image_records),
        )

        return page_records, image_records

    # ============================================================
    # pdfplumber: Tables
    # ============================================================

    def extract_tables(self) -> List[Dict[str, Any]]:
        """Extract tables from every page using pdfplumber."""
        import pdfplumber

        table_records: List[Dict[str, Any]] = []

        try:
            with pdfplumber.open(str(self.pdf_path)) as pdf:
                logger.info(
                    "pdfplumber_opened",
                    pdf_path=str(self.pdf_path),
                )

                for page_index, page in enumerate(pdf.pages):
                    page_number = page_index + 1

                    try:
                        tables = page.extract_tables() or []
                        logger.debug(
                            "tables_extracted_from_page",
                            page_number=page_number,
                            table_count=len(tables),
                        )
                    except Exception as exc:
                        logger.warning(
                            "table_extraction_failed_on_page",
                            pdf_path=str(self.pdf_path),
                            page_number=page_number,
                            error=str(exc),
                        )
                        tables = []

                    for table_index, table in enumerate(tables, start=1):
                        try:
                            if not table:
                                continue

                            # Clean table
                            cleaned_table = []
                            for row in table:
                                cleaned_row = [
                                    cell.strip() if isinstance(cell, str) else cell
                                    for cell in row
                                ]
                                cleaned_table.append(cleaned_row)

                            if not cleaned_table:
                                continue

                            # Convert to DataFrame
                            try:
                                dataframe = pd.DataFrame(
                                    cleaned_table[1:],
                                    columns=cleaned_table[0],
                                )
                            except Exception:
                                dataframe = pd.DataFrame(cleaned_table)

                            table_records.append(
                                {
                                    "page_number": page_number,
                                    "table_index": table_index,
                                    "raw_table": cleaned_table,
                                    "markdown": dataframe.to_markdown(index=False),
                                    "csv": dataframe.to_csv(index=False),
                                }
                            )

                            logger.info(
                                "table_extracted",
                                page_number=page_number,
                                table_index=table_index,
                                rows=len(cleaned_table),
                                columns=len(cleaned_table[0]) if cleaned_table else 0,
                            )
                        except Exception as exc:
                            logger.warning(
                                "table_processing_failed",
                                page_number=page_number,
                                table_index=table_index,
                                error=str(exc),
                            )
                            # Continue processing other tables

        except Exception as exc:
            logger.exception(
                "table_extraction_failed",
                pdf_path=str(self.pdf_path),
                error=str(exc),
            )
            raise DocumentPortalException(
                f"Failed to extract tables from {self.pdf_path}",
                exc,
            ) from exc

        self.table_records = table_records

        logger.info(
            "table_extraction_completed",
            total_tables=len(table_records),
        )

        return table_records

    # ============================================================
    # LangChain Documents (Vision-Compatible)
    # ============================================================

    def create_langchain_documents(self) -> List[Document]:
        """
        Convert parsed content into LangChain Document objects.
        Documents include image paths for multimodal LLM processing.
        """
        documents: List[Document] = []

        try:
            # ============================================================
            # 1. Page Text Documents
            # ============================================================
            for page in self.page_records:
                page_number = page["page_number"]

                documents.append(
                    Document(
                        page_content=page["text"],
                        metadata={
                            "source": str(self.pdf_path),
                            "page_number": page_number,
                            "content_type": "page_text",
                            "character_count": page["character_count"],
                        },
                    )
                )

            logger.info(
                "page_text_documents_created",
                count=len(self.page_records),
            )

            # ============================================================
            # 2. Full Page Image Documents
            # ============================================================
            for page in self.page_records:
                page_number = page["page_number"]
                page_image_path = page["page_image_path"]

                page_image_doc = f"""
PAGE {page_number} - FULL PAGE IMAGE

Image Path: {page_image_path}

🖼️ Vision LLM Integration:
This page image can be sent directly to multimodal LLMs:
- Claude Vision API
- GPT-4V
- Gemini Vision
- LLaVA

The image shows the complete page layout including:
- All text content
- Visual formatting
- Images and diagrams
- Table layouts
"""

                documents.append(
                    Document(
                        page_content=page_image_doc,
                        metadata={
                            "source": str(self.pdf_path),
                            "page_number": page_number,
                            "content_type": "page_image",
                            "image_path": page_image_path,
                            "image_type": "full_page_render",
                            "resolution_scale": self.render_scale,
                        },
                    )
                )

            logger.info(
                "page_image_documents_created",
                count=len(self.page_records),
            )

            # ============================================================
            # 3. Embedded Image Documents
            # ============================================================
            for image in self.image_records:
                page_number = image["page_number"]
                image_index = image["image_index"]
                image_path = image["image_path"]

                image_doc = f"""
EMBEDDED IMAGE - Page {page_number}, Image {image_index}

Image Path: {image_path}

🖼️ Vision LLM Integration:
This embedded image can be sent directly to multimodal LLMs:
- Claude Vision API
- GPT-4V
- Gemini Vision
- LLaVA

Ask the vision LLM to describe, analyze, or extract information
from this image for better RAG context.
"""

                documents.append(
                    Document(
                        page_content=image_doc,
                        metadata={
                            "source": str(self.pdf_path),
                            "page_number": page_number,
                            "content_type": "embedded_image",
                            "image_path": image_path,
                            "image_index": image_index,
                            "image_ext": image["image_ext"],
                            "image_size_bytes": image["image_size_bytes"],
                        },
                    )
                )

            logger.info(
                "embedded_image_documents_created",
                count=len(self.image_records),
            )

            # ============================================================
            # 4. Table Documents
            # ============================================================
            for table in self.table_records:
                page_number = table["page_number"]

                table_text = f"""
TABLE - Page {page_number}, Table {table["table_index"]}

{table["markdown"]}
"""

                documents.append(
                    Document(
                        page_content=table_text,
                        metadata={
                            "source": str(self.pdf_path),
                            "page_number": page_number,
                            "content_type": "table",
                            "table_index": table["table_index"],
                        },
                    )
                )

            logger.info(
                "table_documents_created",
                count=len(self.table_records),
            )

        except Exception as exc:
            logger.exception(
                "langchain_document_creation_failed",
                error=str(exc),
            )
            raise DocumentPortalException(
                "Failed to create LangChain documents",
                exc,
            ) from exc

        self.langchain_docs = documents

        logger.info(
            "langchain_documents_creation_completed",
            total_documents=len(documents),
        )

        return documents

    # ============================================================
    # Save Outputs
    # ============================================================

    @staticmethod
    def _save_json(path: Path, data: Any) -> None:
        """Save data to JSON file with error handling."""
        try:
            with open(path, "w", encoding="utf-8") as file:
                json.dump(
                    data,
                    file,
                    indent=2,
                    ensure_ascii=False,
                    default=str,
                )
            logger.debug(
                "json_file_saved",
                file_path=str(path),
            )
        except Exception as exc:
            logger.exception(
                "json_save_failed",
                file_path=str(path),
                error=str(exc),
            )
            raise DocumentPortalException(
                f"Failed to save JSON file: {path}",
                exc,
            ) from exc

    def save_outputs(self) -> None:
        """Save all parsed records and RAG-ready documents to disk."""

        try:
            logger.info("output_save_started")

            # Save page records
            self._save_json(
                self.output_dir / "page_records.json",
                self.page_records,
            )

            # Save image records
            self._save_json(
                self.output_dir / "image_records.json",
                self.image_records,
            )

            # Save table records
            self._save_json(
                self.output_dir / "table_records.json",
                self.table_records,
            )

            # Save all LangChain Documents as Markdown
            rag_documents_path = self.output_dir / "rag_ready_documents.md"
            with open(rag_documents_path, "w", encoding="utf-8") as file:
                for index, document in enumerate(self.langchain_docs, start=1):
                    file.write(f"\n\n# Document {index}\n")
                    file.write("\nMetadata:\n```json\n")
                    file.write(
                        json.dumps(
                            document.metadata,
                            indent=2,
                            ensure_ascii=False,
                            default=str,
                        )
                    )
                    file.write("\n```\n")
                    file.write("\nContent:\n")
                    file.write(document.page_content)
                    file.write("\n\n---\n")

            logger.info(
                "rag_documents_markdown_saved",
                file_path=str(rag_documents_path),
            )

            # Save tables as Markdown
            tables_path = self.output_dir / "extracted_tables.md"
            with open(tables_path, "w", encoding="utf-8") as file:
                for table in self.table_records:
                    file.write(
                        f"\n\n## Page {table['page_number']} "
                        f"- Table {table['table_index']}\n\n"
                    )
                    file.write(table["markdown"])
                    file.write("\n\n---\n")

            logger.info(
                "extracted_tables_markdown_saved",
                file_path=str(tables_path),
            )

            logger.info(
                "output_save_completed",
                output_dir=str(self.output_dir),
            )

        except Exception as exc:
            logger.exception(
                "output_save_failed",
                error=str(exc),
            )
            raise DocumentPortalException(
                "Failed to save outputs",
                exc,
            ) from exc

    # ============================================================
    # Main Pipeline
    # ============================================================

    def parse(self, save_output: bool = True) -> Dict[str, Any]:
        """
        Run the complete multimodal parsing pipeline.

        Args:
            save_output: Whether to save outputs to disk

        Returns:
            {
                "pages": [...],
                "images": [...],
                "tables": [...],
                "documents": [LangChain Document, ...],
                "output_dir": "...",
                "image_dir": "...",
                "page_image_dir": "..."
            }
        """
        logger.info(
            "pdf_parsing_pipeline_started",
            pdf_path=str(self.pdf_path),
        )

        try:
            # Extract text and images
            logger.info("extracting_text_and_images")
            self.extract_text_and_images()

            # Extract tables
            logger.info("extracting_tables")
            self.extract_tables()

            # Create LangChain documents
            logger.info("creating_langchain_documents")
            self.create_langchain_documents()

            # Save outputs
            if save_output:
                logger.info("saving_outputs")
                self.save_outputs()

            result = {
                "pages": self.page_records,
                "images": self.image_records,
                "tables": self.table_records,
                "documents": self.langchain_docs,
                "output_dir": str(self.output_dir),
                "image_dir": str(self.image_dir),
                "page_image_dir": str(self.page_image_dir),
            }

            logger.info(
                "pdf_parsing_pipeline_completed_successfully",
                pages=len(self.page_records),
                images=len(self.image_records),
                tables=len(self.table_records),
                documents=len(self.langchain_docs),
            )

            return result

        except DocumentPortalException:
            raise
        except Exception as exc:
            logger.exception(
                "pdf_parsing_pipeline_failed",
                pdf_path=str(self.pdf_path),
                error=str(exc),
            )
            raise DocumentPortalException(
                f"Failed to parse PDF: {self.pdf_path}",
                exc,
            ) from exc


# ============================================================
# Example Usage
# ============================================================

if __name__ == "__main__":

    logger.info("main_execution_started")

    try:
        # 📁 DATA PATHS
        DATA_DIR = Path(r"C:\Users\Admin\Agentic AI Projects\AI\RAG\Langchain-use\data")

        PDF_PATH = DATA_DIR / "Client_Contracts_Policies_and_Incident_Records.pdf"
        OUTPUT_DIR = DATA_DIR / "parsed_pdf_output"

        logger.info(
            "configuration_loaded",
            data_dir=str(DATA_DIR),
            pdf_path=str(PDF_PATH),
            output_dir=str(OUTPUT_DIR),
        )

        # Initialize parser
        parser = MultimodalPDFParser(
            pdf_path=str(PDF_PATH),
            output_dir=str(OUTPUT_DIR),
            render_scale=2.0,
        )

        # Run parsing pipeline
        result = parser.parse(save_output=True)

        # Extract documents
        documents = result["documents"]

        # Print summary
        print("\n" + "="*60)
        print("MULTIMODAL PARSING SUMMARY")
        print("="*60)
        print(f"📄 Pages:                  {len(result['pages'])}")
        print(f"🖼️  Embedded Images:       {len(result['images'])}")
        print(f"📊 Tables:                 {len(result['tables'])}")
        print(f"📚 LangChain Documents:    {len(documents)}")
        print(f"📂 Text Output Directory:  {result['output_dir']}")
        print(f"🖼️  Image Directory:        {result['image_dir']}")
        print(f"📄 Page Image Directory:   {result['page_image_dir']}")
        print("="*60 + "\n")

        # Preview documents by type
        print("DOCUMENT TYPES IN RAG:")
        print("-" * 60)
        doc_types = {}
        for doc in documents:
            content_type = doc.metadata.get("content_type", "unknown")
            doc_types[content_type] = doc_types.get(content_type, 0) + 1

        for dtype, count in sorted(doc_types.items()):
            print(f"  {dtype:20s}: {count:3d} documents")

        logger.info(
            "main_execution_completed_successfully",
            documents_created=len(documents),
        )

        print("\n" + "="*60)
        print("✅ Ready for Vision LLM Integration!")
        print("="*60 + "\n")

    except DocumentPortalException as exc:
        logger.exception("document_portal_exception", error=str(exc))
        print(f"\n❌ Document Portal Exception: {exc}")
        sys.exit(1)
    except Exception as exc:
        logger.exception("unexpected_exception", error=str(exc))
        print(f"\n❌ Unexpected Exception: {exc}")
        sys.exit(1)
