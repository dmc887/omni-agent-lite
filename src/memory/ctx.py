from __future__ import annotations

from asyncio import Lock

from typing import Optional, Dict, List


class Context:
    def __init__(
        self, 
        size: Optional[int] = None, 
        size_t: Optional[int] = None
    ):
        self._memory: List[Dict[str, str]] = []
        self._lock = Lock()

        self.size = size
        self.size_t = size_t

        self._cached_size_t = 0

    @property
    def memory(self) -> List[Dict[str, str]]:
        if len(self._memory()) > self.size \
                 or self._cached_size_t > self.size_t:
            self._memory = []
        return self._memory

    @memory.setter
    def memory_setter(self, *message: Dict[str, str]) -> None:
        for msg in message:
            if "user" in msg:
                self._memory.append(msg)

    async def add(
        self, 
        user: str, 
        model: Optional[str] = None,
        system: Optional[str] = None
    ) -> int:
        row = {"user": user, "model": model, "system": system}
        async with self._lock:
            self._memory.append(row)
            index = len(self._memory) - 1
            
            self._cached_size_t += len(row)
        return index

    async def remove(self, index: int) -> bool:
        async with self._lock:
            res = self._memory.pop(index)
        return res == True

    def clear(self) -> None:
        self._memory.clear()
