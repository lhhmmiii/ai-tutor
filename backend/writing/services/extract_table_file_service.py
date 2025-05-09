import os
import sys
from datetime import datetime
from io import BytesIO

import pandas as pd
from fastapi import HTTPException
from llama_index.core import Document
from writing.services.base_service import TextExtractor
from writing.helpers.excel_csv_helper import (
    delete_meaningless_columns,
    delete_meaningless_rows,
)
from writing.utils.format_time_utils import _format_file_timestamp


class TableFile(TextExtractor):
    def __init__(self, is_header=False):
        self.is_header = is_header

    async def extract_text(self, file):
        file_content = await file.read()
        _, file_extension = os.path.splitext(file.filename)
        try:
            byte_stream = BytesIO(file_content)
            if file_extension == ".csv":
                if not self.is_header:
                    data = pd.read_csv(byte_stream, header=None)
                else:
                    data = pd.read_csv(byte_stream)
            elif file_extension in [".xlsx", ".xls"]:
                all_sheets = pd.read_excel(
                    byte_stream,
                    sheet_name=None,
                    header=None if not self.is_header else 0,
                )
                sheet_texts = []
                sheet_names = []
                for sheet_name, df in all_sheets.items():
                    data = delete_meaningless_columns(df)
                    data = delete_meaningless_rows(data)
                    sheet_texts.append(self._process_data(data))
                    sheet_names.append(sheet_name)
                return sheet_texts, sheet_names
            else:
                raise ValueError("Unsupported file type. Use 'csv' or 'excel'.")

            data = delete_meaningless_columns(data)
            data = delete_meaningless_rows(data)
            return [self._process_data(data)], []

        except HTTPException as e:
            raise e

    def supports_file_type(self, file_name):
        _, file_extension = os.path.splitext(file_name)
        return file_extension in [".xlsx", ".xls", ".csv"]

    def create_docs(self, texts, file_name, sheet_names, user_id):
        docs = []
        for i, text in enumerate(texts):
            metadata = {}
            metadata["total_sheet"] = len(texts)
            if sheet_names:
                metadata["sheet_name"] = sheet_names[i]
            metadata["creation_date"] = _format_file_timestamp(
                timestamp=datetime.now().timestamp(), include_time=True
            )
            metadata["file_name"] = str(file_name)
            metadata["user_id"] = user_id
            metadata["source"] = i + 1
            doc = Document(text=text, extra_info=metadata)
            docs.append(doc)
        return docs

    def _process_data(self, data):
        list_column_names = data.columns
        list_values = data.values

        if not self.is_header:
            list_column_names = [
                f"Column {i + 1}" for i in range(len(list_column_names))
            ]
        elif self.is_header and "Unnamed" in list_column_names[0]:
            list_column_names = list_values[0]
            list_values = list_values[1:]

        text = ""
        for value in list_values:
            for i, column_name in enumerate(list_column_names):
                text += f"{column_name}: {value[i]}\n"
        return text
