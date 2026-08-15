from abc import ABC, abstractmethod

from httpx import AsyncClient, Response

from typing import Any


class BaseHTTP(ABC):
    def __init__(self, **httpx_kw: Any):
        self._session = None
        self._kw = httpx_kw

    @property
    def session(self) -> AsyncClient:
        if self._session is None or self._session.is_closed:
            self._session = AsyncClient(**self._kw)

        return self._session

    @abstractmethod
    async def request(self,  *args: Any, **kwargs: Any) -> Response:
        ...
