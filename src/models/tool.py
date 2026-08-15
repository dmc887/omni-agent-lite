from abc import ABC, abstractmethod

from typing import Any


class BaseTool(ABC):
    def __init__(self) -> None:
        ...
        
    @abstractmethod
    async def __call__(self, *args: Any, **kwargs: Any) -> Any:
        ...
