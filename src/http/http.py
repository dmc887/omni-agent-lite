from ..models import BaseHTTP

from httpx import Response
from http import HTTPMethod

from typing import Any, Dict, Union


class HTTPClient(BaseHTTP):
    def __init__(self, **httpx_kw: Any):
        super().__init__(**httpx_kw)

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
