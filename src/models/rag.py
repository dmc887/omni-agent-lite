from abc import ABC, abstractmethod

from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_community.vectorstores import FAISS

from typing import List, Any


class BaseRAG(ABC):
    def __init__(self, embeddings: Embeddings):
        self.embeddings = embeddings
        self._vectorstore: FAISS = None

    @abstractmethod
    async def load_documents(self, *args: Any, **kwargs: Any) -> None:
        ...

    async def search(self, query: str, top_k: int = 3) -> "List[Document]":
        if not self._vectorstore:
            raise ValueError("FAISS индекс пуст")
            
        return await self._vectorstore.asimilarity_search(query, k=top_k)
