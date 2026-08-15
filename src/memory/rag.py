from ..models import BaseRAG, Doc

from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_community.vectorstores import FAISS

from typing import List


class RAG(BaseRAG):
    def __init__(self, embeddings: Embeddings):
        super().__init__(embeddings=embeddings)

    async def load_documents(self, *docs: "Doc") -> None:
        buff = [Document(doc.text, metadata=doc.metadata) for doc in docs]
            
        self._vectorstore = await FAISS.afrom_documents(buff, self.embeddings)
