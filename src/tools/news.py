import xml.etree.ElementTree as ET

from ..models import BaseTool, HTTPClient

from typing import Dict, Optional


class NewsTool(BaseTool):
    def __init__(
        self, 
        url: str = "https://news.google.com",
        rss_path: str = "/rss?hl=ru&gl=RU&ceid=RU:ru"
    ):
        super().__init__()
        
        self.http = HTTPClient(base_url=url)
        self.rss_path = rss_path

    async def __call__(
        self, 
        count: Optional[int] = 1,
        page: Optional[int] = 0
    ) -> Dict[str, str]:
        """
        Получает список новостей через RSS.
        
        :param count: Количество новостей, int default=1
        :param page: Страница, int default=0

        :returns Dict[str, str]: Список новостей с ссылкой на источник
        """
        response = await self.http.request(url=self.rss_path)
        
        xml_data = response.text
        
        root = ET.fromstring(xml_data)
        items = root.findall(".//item")
        
        end_index = page + (count or 1)
        
        buff = {}
        for index, item in enumerate(items[page:end_index]):
            buff[index] = {
                "title": item.find("title").text,
                "source": item.find("link").text \
                    if item.find("link") is not None else None
            }
                
        return buff
