from ..models import HTTPClient, BaseTool

from typing import (
    Dict, 
    Optional, 
    List, 
    Union
)


class CryptoTool(BaseTool):
    def __init__(
        self, 
        base_url: str = "https://api.binance.com",
        ticker_path: str = "/api/v3/ticker/price"
    ):

        self.http = HTTPClient(base_url=base_url)
        self.ticker_path = ticker_path

    async def __call__(
        self, 
        symbols: Optional[Union[str, List[str]]] = "BTC",
        vs_currency: Optional[str] = "RUB",
        return_only_value: Optional[bool] = True
    ) -> Dict[str, Union[str, Dict[str, str]]]:
        """
        Получает текущий курс криптовалют.
        
        :param symbols: Строка или список строк с валютой, Optional[Union[str, List[str]]]  default=BTC
        :param vs_currency: Базовая валюта для оценки, Optional[str] default=RUB
        :param return_only_value: Если True, вернет {тикер: цена}. Если False, вернет {тикер: {"symbol": ..., "price": ...}}, default=True

        :returns Dict[str, Union[str, Dict[str, str]]]: вернет {symbol: price in vs_currency, ...}, либо 
        {symbol: {pair: ..., price: ...}}
        """
        vs_currency = vs_currency.upper()
        
        if isinstance(symbols, str):
            target_symbols = [symbols.upper()]
        else:
            target_symbols = [s.upper() for s in symbols]

        result = {}

        for crypto in target_symbols:
            pair = f"{crypto}{vs_currency}"
            
            try:
                response = await self.http.request(
                    url=f"{self.ticker_path}?symbol={pair}", 
                    method="GET"
                )
                
                data = response.json()
                
                if "price" in data:
                    price = str(float(data["price"]))
                    
                    if return_only_value:
                        result[crypto] = price
                    else:
                        result[crypto] = {
                            "pair": data["symbol"],
                            "price": price,
                            "vs_currency": vs_currency
                        }
                else:
                    result[crypto] = "Данные не найдены"
                    
            except Exception as e:
                result[crypto] = f"Ошибка запроса: {e}"

        return result
