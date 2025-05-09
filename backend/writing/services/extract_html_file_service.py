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


class HtmlFile(TextExtractor):
    def __init__(self, default_encoding="utf-8"):
        self.default_encoding = default_encoding

    async def extract_text(self, file, url=None):
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
        except HTTPException as e:
            raise e

    def supports_file_type(self, file_name: str, url: str):
        if url:
            return True
        else:
            _, file_extension = os.path.splitext(file_name)
            return file_extension == ".html"

    def create_docs(self, texts: list[Any], file_name: str, url: str, user_id: str):
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
