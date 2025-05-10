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

    def set_is_header(self, is_header: bool):
        self.is_header = is_header

    async def extract_text(self, file):
        file_content = await file.read()
        _, file_extension = os.path.splitext(file.filename)
        try:
            byte_stream = BytesIO(file_content)
            if file_extension == ".csv":
                data = pd.read_csv(byte_stream, header=0 if self.is_header else None)
            elif file_extension in [".xlsx", ".xls"]:
                return self._process_excel(byte_stream)
            else:
                raise ValueError("Unsupported file type. Use 'csv' or 'excel'.")

            return self._process_single_sheet(data)

        except HTTPException as e:
            raise e

    def _process_excel(self, byte_stream):
        all_sheets = pd.read_excel(
            byte_stream,
            sheet_name=None,
            header=0 if self.is_header else None
        )
        sheet_texts = []
        sheet_names = []
        for sheet_name, df in all_sheets.items():
            processed_data = self._clean_and_process_data(df)
            sheet_texts.append(processed_data)
            sheet_names.append(sheet_name)
        return sheet_texts, sheet_names

    def _process_single_sheet(self, data):
        processed_data = self._clean_and_process_data(data)
        return [processed_data], []

    def _clean_and_process_data(self, data):
        data = delete_meaningless_columns(data)
        data = delete_meaningless_rows(data)
        return self._process_data(data)

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
        column_names = data.columns
        values = data.values
        column_names = [str(col) if isinstance(col, int) else col for col in column_names]
        if not self.is_header:
            column_names = [
                f"Column {i + 1}" for i in range(len(column_names))
            ]
        elif self.is_header and "Unnamed" in column_names[0]:
            column_names = values[0]
            values = values[1:]

        text = ""
        for value in values:
            for i, column_name in enumerate(column_names):
                text += f"{column_name}: {value[i]}\n"
        return text
