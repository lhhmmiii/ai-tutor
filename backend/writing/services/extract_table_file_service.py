import os
import sys
from datetime import datetime
from io import BytesIO
from typing import Any
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
    """
    A class for extracting text from table-based file formats including Excel and CSV files.
    
    This class provides methods to:
    - Extract text from Excel and CSV files
    - Process multiple sheets from Excel files
    - Clean and format table data
    - Create document objects with metadata
    
    Attributes:
        is_header (bool): Flag indicating whether the file has headers
    """

    def __init__(self, is_header: bool = False):
        self.is_header = is_header

    def set_is_header(self, is_header: bool):
        """Set whether the file has headers.
        
        Args:
            is_header (bool): Flag indicating whether the file has headers
        """
        self.is_header = is_header

    async def extract_text(self, file: Any) -> tuple[list[str], list[str]]:
        """
        Extract text from a table file (Excel or CSV).
        
        Args:
            file: The file object to extract text from
            
        Returns:
            tuple: A tuple containing (list of processed texts, list of sheet names)
            
        Raises:
            HTTPException: If there's an error reading the file or unsupported file type
        """
        try:
            file_content = await file.read()
            _, file_extension = os.path.splitext(file.filename)
            byte_stream = BytesIO(file_content)
            
            if file_extension == ".csv":
                data = pd.read_csv(byte_stream, header=0 if self.is_header else None)
            elif file_extension in [".xlsx", ".xls"]:
                return self._process_excel(byte_stream)
            else:
                raise HTTPException(
                    status_code=400,
                    detail="Unsupported file type. Please use CSV or Excel files."
                )

            return self._process_single_sheet(data)

        except pd.errors.EmptyDataError:
            raise HTTPException(
                status_code=400,
                detail="The file appears to be empty or corrupted."
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error processing table file: {str(e)}"
            )

    def _process_excel(self, byte_stream: BytesIO) -> tuple[list[str], list[str]]:
        """
        Process an Excel file with multiple sheets.
        
        Args:
            byte_stream: BytesIO object containing the Excel file
            
        Returns:
            tuple: (list of processed texts, list of sheet names)
            
        Raises:
            HTTPException: If there's an error reading the Excel file
        """
        try:
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
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error processing Excel file: {str(e)}"
            )

    def _process_single_sheet(self, data: pd.DataFrame) -> tuple[list[str], list[str]]:
        """
        Process a single sheet of data.
        
        Args:
            data: DataFrame containing the sheet data
            
        Returns:
            tuple: (list containing single processed text, empty list for sheet names)
        """
        processed_data = self._clean_and_process_data(data)
        return [processed_data], []

    def _clean_and_process_data(self, data: pd.DataFrame) -> str:
        """
        Clean and process the table data.
        
        Args:
            data: DataFrame to process
            
        Returns:
            str: Processed text representation of the data
        """
        data = delete_meaningless_columns(data)
        data = delete_meaningless_rows(data)
        return self._process_data(data)

    def supports_file_type(self, file_name: str) -> bool:
        """
        Check if the file type is supported.
        
        Args:
            file_name (str): Name of the file to check
            
        Returns:
            bool: True if the file type is supported, False otherwise
        """
        _, file_extension = os.path.splitext(file_name)
        return file_extension in [".xlsx", ".xls", ".csv"]

    def create_docs(self, texts, file_name, sheet_names, user_id):
        """
        Create document objects with metadata from processed texts.
        
        Args:
            texts (list): List of processed text strings
            file_name (str): Name of the original file
            sheet_names (list): List of sheet names (for Excel files)
            user_id (str): ID of the user who uploaded the file
            
        Returns:
            list: List of Document objects with metadata
        """
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

    def _process_data(self, data: pd.DataFrame) -> str:
        """
        Process the table data into a text format.
        
        Args:
            data: DataFrame to process
            
        Returns:
            str: Formatted text representation of the table data
        """
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
