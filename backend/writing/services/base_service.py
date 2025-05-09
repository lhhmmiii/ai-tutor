from abc import ABC, abstractmethod
from typing import Any


class TextExtractor(ABC):
    @abstractmethod
    async def extract_text(self, file, url: str = None):
        """
        Extract text from the given source.
        :param file: Uploaded file
        :param url: The url.
        :param is_header: Table file have header or not.
        :return: Extracted text or document object.
        """
        pass

    @abstractmethod
    def supports_file_type(self, file_name: str, url: str = None):
        """
        Check if the extractor supports a specific file type.
        :param file_extension: The file extension or MIME type.
        :return: Boolean indicating support.
        """
        pass

    @abstractmethod
    def create_docs(
        self,
        texts: list[Any] = None,
        file_name: str = None,
        url: str = None,
        sheet_names: str = None,
        user_id: str = None,
    ):
        """
        Create nodes from text
        :param texts: Extracted text from file
        :param metadatas: Metadata
        :param sheet_names: sheet name(for excel file)
        :user_id: identity of user
        """
        pass


class BaseQA(ABC):
    @abstractmethod
    def query(self, query_str, user_id: None):
        """
        Answer the questions from user
        query_str: query from user
        user_id: user identity
        """
        pass

    @abstractmethod
    def create_query_engine_tool(self):
        """
        Create query engine tool for Agent
        """
        pass
