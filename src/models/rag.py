from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_community.vectorstores import FAISS

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import List
    from .doc import Doc


class BaseRAG:
    def __init__(self, embeddings: Embeddings):
        self.embeddings = embeddings
        self._vectorstore = None

    def load_documents(self, *docs: "Doc") -> None:
        """Строит FAISS индекс по обьектам Doc"""
        buff = [Document(doc.text, metadata=doc.metadata) for doc in docs]
            
        self._vectorstore = FAISS.from_documents(buff, self.embeddings)

    def search(self, query: str, top_k: int = 3) -> "List[Document]":
        if not self._vectorstore:
            raise ValueError("FAISS индекс пуст")
            
        return self._vectorstore.similarity_search(query, k=top_k)
