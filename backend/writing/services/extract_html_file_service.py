import os
import re
import sys
from datetime import datetime
from typing import Any

import requests
from bs4 import BeautifulSoup
from fastapi import HTTPException
from llama_index.core import Document
from writing.services.base_service import TextExtractor
from writing.utils.format_time_utils import _format_file_timestamp
from typing import Optional, Any

class HtmlFile(TextExtractor):
    """
    A class for extracting text from HTML files or URLs.
    """

    def __init__(self, default_encoding: Optional[str] = "utf-8"):
        self.default_encoding = default_encoding

    async def extract_text(self, file: Any, url: Optional[str] = None) -> list[str]:
        """
        Extract text from an HTML file or URL.

        Args:
            file: The HTML file to process.
            url: The URL to fetch HTML content from.

        Returns:
            A list containing the extracted text.

        Raises:
            HTTPException: If there's an error during text extraction.
        """
        try:
            if url:
                response = requests.get(url)
                content = response.content
            else:
                file_content = await file.read()
                content = file_content.decode(self.default_encoding)
            soup = BeautifulSoup(content, "html.parser")
            text = soup.get_text()
            text = re.sub(r"\n+", "\n", text)
            return [text]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error extracting text: {str(e)}")

    def supports_file_type(self, file_name: str, url: str) -> bool:
        """
        Check if the file type or URL is supported.

        Args:
            file_name: The name of the file.
            url: The URL to check.

        Returns:
            True if the file type or URL is supported, False otherwise.
        """
        if url:
            return True
        else:
            _, file_extension = os.path.splitext(file_name)
            return file_extension == ".html"

    def create_docs(self, texts: list[Any], file_name: str, url: str, user_id: str) -> list[Document]:
        """
        Create Document objects from extracted texts.

        Args:
            texts: List of extracted texts.
            file_name: Name of the processed file.
            url: URL of the processed content.
            user_id: ID of the user who initiated the process.

        Returns:
            A list of Document objects.

        Raises:
            HTTPException: If there's an error during document creation.
        """
        try:
            docs = []
            for i, text in enumerate(texts):
                metadata = {}
                metadata["creation_date"] = _format_file_timestamp(
                    timestamp=datetime.now().timestamp(), include_time=True
                )
                if file_name != "":
                    metadata["file_name"] = str(file_name)
                else:
                    metadata["url"] = str(url)
                metadata["user_id"] = user_id
                metadata["source"] = i + 1
                doc = Document(text=text, extra_info=metadata)
                docs.append(doc)
            return docs
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error creating documents: {str(e)}")
