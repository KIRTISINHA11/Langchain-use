# -*- coding: utf-8 -*-
"""
vision_rag.py

Integrate extracted PDF images with Vision LLMs in RAG pipeline.

Supports:
- Claude Vision API
- GPT-4V (OpenAI)
- Gemini Vision (Google)
- LLaVA and other open-source vision models
"""

import base64
from pathlib import Path
from typing import Optional


class VisionRAGIntegration:
    """
    Helper class to process extracted PDF images for Vision LLM integration.
    """

    @staticmethod
    def encode_image_to_base64(image_path: str | Path) -> str:
        """
        Encode image to base64 for API transmission.

        Args:
            image_path: Path to image file

        Returns:
            Base64 encoded image string
        """
        with open(image_path, "rb") as image_file:
            return base64.standard_b64encode(image_file.read()).decode("utf-8")

    @staticmethod
    def create_claude_vision_message(
        image_path: str | Path,
        query: str,
        image_media_type: str = "image/png"
    ) -> dict:
        """
        Create Claude Vision API message with image.

        Args:
            image_path: Path to image file
            query: Question/query about the image
            image_media_type: MIME type (image/png, image/jpeg, image/gif, image/webp)

        Returns:
            Message dict for Claude API

        Example:
            >>> message = VisionRAGIntegration.create_claude_vision_message(
            ...     image_path="page_001.png",
            ...     query="What are the main topics on this page?"
            ... )
            >>> response = client.messages.create(
            ...     model="claude-3-5-sonnet-20241022",
            ...     max_tokens=1024,
            ...     messages=[message]
            ... )
        """
        image_data = VisionRAGIntegration.encode_image_to_base64(image_path)

        return {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": image_media_type,
                        "data": image_data,
                    },
                },
                {
                    "type": "text",
                    "text": query
                }
            ],
        }

    @staticmethod
    def create_gpt4v_vision_message(
        image_path: str | Path,
        query: str,
        image_media_type: str = "image/png"
    ) -> dict:
        """
        Create GPT-4V API message with image.

        Args:
            image_path: Path to image file
            query: Question/query about the image
            image_media_type: MIME type (image/png, image/jpeg, image/gif, image/webp)

        Returns:
            Message dict for OpenAI API

        Example:
            >>> message = VisionRAGIntegration.create_gpt4v_vision_message(
            ...     image_path="page_001.png",
            ...     query="Extract all text from this image"
            ... )
            >>> response = client.chat.completions.create(
            ...     model="gpt-4-vision-preview",
            ...     messages=[message],
            ...     max_tokens=1024
            ... )
        """
        image_data = VisionRAGIntegration.encode_image_to_base64(image_path)

        return {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:{image_media_type};base64,{image_data}",
                        "detail": "high"
                    },
                },
                {
                    "type": "text",
                    "text": query
                }
            ],
        }

    @staticmethod
    def create_gemini_vision_message(
        image_path: str | Path,
        query: str
    ) -> dict:
        """
        Create Google Gemini Vision API message with image.

        Args:
            image_path: Path to image file
            query: Question/query about the image

        Returns:
            Message dict for Gemini API

        Example:
            >>> message = VisionRAGIntegration.create_gemini_vision_message(
            ...     image_path="page_001.png",
            ...     query="Describe the layout and content of this page"
            ... )
            >>> response = client.generate_content([
            ...     message
            ... ])
        """
        image_data = VisionRAGIntegration.encode_image_to_base64(image_path)

        return {
            "image": {
                "data": image_data
            },
            "text": query
        }

    @staticmethod
    def extract_info_from_page_image(
        image_path: str | Path,
        query: str = "Please describe all content, text, images, and layout of this page in detail."
    ) -> str:
        """
        Example query to extract information from page image.

        Returns:
            Detailed description to use in RAG context
        """
        return f"""
Vision LLM Task: Analyze Page Image

Image Path: {image_path}
Query: {query}

Expected Output:
- All visible text content
- Descriptions of images/diagrams
- Table structures and content
- Document layout
- Important visual elements
- Any handwritten notes or annotations
"""

    @staticmethod
    def extract_info_from_embedded_image(
        image_path: str | Path,
        query: str = "Please describe this image in detail including what it depicts, any text, important elements, and context."
    ) -> str:
        """
        Example query to extract information from embedded image.

        Returns:
            Detailed description to use in RAG context
        """
        return f"""
Vision LLM Task: Analyze Embedded Image

Image Path: {image_path}
Query: {query}

Expected Output:
- What the image shows
- Relevant text within the image
- Key details and elements
- Context about the image
- Relevance to the document
"""


# ============================================================
# Example Usage
# ============================================================

if __name__ == "__main__":

    from data_parsing import MultimodalPDFParser

    # Step 1: Parse PDF to extract images
    print("Step 1: Parsing PDF to extract images...")
    print("="*60)

    DATA_DIR = Path(r"C:\Users\Admin\Agentic AI Projects\AI\RAG\Langchain-use\data")
    PDF_PATH = DATA_DIR / "Client_Contracts_Policies_and_Incident_Records.pdf"
    OUTPUT_DIR = DATA_DIR / "parsed_pdf_output"

    parser = MultimodalPDFParser(
        pdf_path=str(PDF_PATH),
        output_dir=str(OUTPUT_DIR),
    )

    result = parser.parse(save_output=True)
    documents = result["documents"]

    # Step 2: Filter vision documents (images)
    print("\n\nStep 2: Filtering image documents for vision LLM...")
    print("="*60)

    vision_docs = [
        doc for doc in documents
        if doc.metadata.get("content_type") in ["page_image", "embedded_image"]
    ]

    print(f"Found {len(vision_docs)} vision-compatible documents\n")

    # Step 3: Show how to use with Vision LLMs
    print("\nStep 3: Example - Creating Vision LLM prompts...")
    print("="*60)

    for i, doc in enumerate(vision_docs[:3], 1):
        image_path = doc.metadata.get("image_path")
        content_type = doc.metadata.get("content_type")

        print(f"\n📸 Document {i}: {content_type}")
        print(f"   Image: {image_path}")

        if content_type == "page_image":
            prompt = VisionRAGIntegration.extract_info_from_page_image(image_path)
        else:
            prompt = VisionRAGIntegration.extract_info_from_embedded_image(image_path)

        print(f"   Prompt Preview:\n{prompt[:300]}...")

    # Step 4: Show encoding example
    print("\n\nStep 4: Example - Encoding image for API...")
    print("="*60)

    if vision_docs:
        example_image = vision_docs[0].metadata.get("image_path")
        if Path(example_image).exists():
            encoded = VisionRAGIntegration.encode_image_to_base64(example_image)
            print(f"✓ Image encoded to base64")
            print(f"  Length: {len(encoded)} characters")
            print(f"  Preview: {encoded[:50]}...")
        else:
            print(f"⚠ Image file not found: {example_image}")

    # Step 5: Show message creation examples
    print("\n\nStep 5: Example - Creating API messages...")
    print("="*60)

    if vision_docs and Path(vision_docs[0].metadata.get("image_path")).exists():
        example_image = vision_docs[0].metadata.get("image_path")

        # Claude message
        claude_msg = VisionRAGIntegration.create_claude_vision_message(
            image_path=example_image,
            query="What is the main content of this page?"
        )
        print(f"✓ Claude Vision message created")
        print(f"  Supports: claude-3-5-sonnet, claude-3-opus, etc.")

        # GPT-4V message
        gpt_msg = VisionRAGIntegration.create_gpt4v_vision_message(
            image_path=example_image,
            query="What is the main content of this page?"
        )
        print(f"✓ GPT-4V message created")
        print(f"  Supports: gpt-4-vision-preview, gpt-4-turbo")

        # Gemini message
        gemini_msg = VisionRAGIntegration.create_gemini_vision_message(
            image_path=example_image,
            query="What is the main content of this page?"
        )
        print(f"✓ Gemini Vision message created")
        print(f"  Supports: gemini-pro-vision, gemini-1.5-pro")

    print("\n" + "="*60)
    print("✅ Vision RAG Integration Ready!")
    print("="*60 + "\n")
