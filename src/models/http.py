from httpx import AsyncClient, Response
from http import HTTPMethod

from typing import Any, Union, Dict


class HTTPClient:
    def __init__(self, **httpx_kw: Any):
        self._session = None
        self._kw = httpx_kw

    @property
    def session(self) -> AsyncClient:
        if self._session is None or self._session.is_closed:
            self._session = AsyncClient(**self._kw)

        return self._session

    async def request(
        self,  
        url: str, 
        method: HTTPMethod = HTTPMethod.GET,
        data: Union[str, Dict[Any, Any]] = None,
        headers: Dict[str, str] = None
    ) -> Response:
        if not method in HTTPMethod:
            raise ValueError("Incorrect HTTP method")
        
        req = await self.session.request(
            method=method,
            url=url,
            data=data,
            headers=headers
        )
        req.raise_for_status()
        
        return req
