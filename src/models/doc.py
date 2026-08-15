from __future__ import annotations

from pydantic import BaseModel

from pathlib import Path
from typing import Dict, Any


class Doc(BaseModel):
    title: str
    text: str

    @property
    def metadata(self) -> Dict[str, Any]:
        return {"title": self.title}

    @classmethod
    def from_file(cls, path: str, encoding: str = "utf-8") -> Doc:
        fp = Path(path)
        with open(fp, mode="r", encoding=encoding) as f:
            data = f.read()

        return cls(title=fp.stem, text=data)
