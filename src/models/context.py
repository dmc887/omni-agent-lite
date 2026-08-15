from __future__ import annotations

from asyncio import Lock

from typing import Optional, List, Dict


class Context:
    def __init__(self, size: Optional[int] = None):
        self._memory: List[Dict[str, str]] = []
        self._lock = Lock()

    @property
    def memory(self) -> List[Dict[str, str]]:
        return self._memory

    @memory.setter
    def memory_setter(self, *message: Dict[str, str]) -> None:
        for msg in message:
            if "user" in msg:
                self._memory.append(msg)

    async def add(
        self, 
        user: str, 
        model: str,
        system: Optional[str] = None
    ) -> int:
        row = {"user": user, "model": model, "system": system}
        async with self._lock:
            self._memory.append(row)

            index = len(self._memory) - 1
        return index

    async def remove(self, index: int) -> bool:
        async with self._lock:
            res = self._memory.pop(index)
        return res == True
