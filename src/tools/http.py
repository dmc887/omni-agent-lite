from ..models import BaseTool
from ..http import HTTPClient

from typing import Any, Union, Dict
from httpx import Response


class HTTPTool(BaseTool):
    def __init__(self, **httpx_kw: Any):
        super().__init__()

        self.http = HTTPClient(**httpx_kw)

    async def request(
        self,  
        url: str, 
        method: str,
        data: Union[str, Dict[Any, Any]] = None,
        headers: Dict[str, str] = None
    ) -> Response:
        """
        Выполняет асинхронный HTTP-запрос

        :param url: URL
        :param method: HTTP метод
        :param data: Тело запроса в виде dict/str
        :param headers: HTTP заголовки

        :returns httpx.Response: объект ответа httpx, содержащий .text, .json(), .status_code
        """
        return await self.http.request(
            url=url,
            method=method,
            data=data,
            headers=headers
        )
