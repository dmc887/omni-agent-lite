from ..models import BaseTool

import os

from pathlib import Path
from typing import Dict, Optional


class FSTool(BaseTool):
    def __init__(self, sandbox_dir: Optional[str] = None):
        if sandbox_dir:
            self.sandbox_path = Path(sandbox_dir).resolve()
        else:
            self.sandbox_path = Path(os.getcwd()).resolve()

    def _verify_path(self, path: str) -> Path:
        """
        Защитная функция: проверяет, находится ли путь внутри разрешенной директории
        """
        resolved_path = (self.sandbox_path / path).resolve()
        
        if not str(resolved_path).startswith(str(self.sandbox_path)):
            raise PermissionError(
                f"К {path} доступ запрещен"
            )
        return resolved_path

    def read(self, file_path: str) -> Dict[str, str]:
        """
        Читает содержимое определенного файла

        :param file_path: путь к файлу

        :returns Dict[str, str]: Пример {"status": "success", "content": content}
        """
        try:
            path = self._verify_path(file_path)
            if not path.is_file():
                return {"status": "error", "error": f"Файл '{file_path}' не существует"}
                
            content = path.read_text(encoding="utf-8")
            return {"status": "success", "content": content}
        except Exception as e:
            return {"status": "error", "error": str(e)}

    def write(self, file_path: str, content: str, mode: str = "w") -> Dict[str, str]:
        """
        Записывает или дописывает данные в файл
        
        :param mode: 'w' для перезаписи, 'a' для добавления текста в конец файла
        
        :returns Dict[str, str]: Пример {"status": "success"}
        """
        try:
            if mode not in ["w", "a"]:
                raise ValueError("Неверный режим записи. Только 'w' или 'a'")
                
            safe_path = self._verify_path(file_path)
                        
            with open(safe_path, mode, encoding="utf-8") as f:
                f.write(content)
                
            return {"status": "success"}
        except Exception as e:
            return {"status": "error", "error": str(e)}


    async def __call__(
        self,
        mode: str,
        file_path: str,
        content: str = None,
        write_mode: str = "w"
    ) -> None:
        """
        Интерфейс для чтения или записи файлов в текущей директории

        :param mode: Режим работы 'read' или 'write'
        :param file_path: Относительный путь к файлу внутри песочницы
        :param content: Текст для записи, используется только в режиме 'write'
        :param write_mode: Режим записи: 'w' или 'a', используется только в режиме 'write'

        :returns read: вернет {"status": "success", "content": ...} для чтения
        :returns write: вернет {"status": "success"} для записи
        """
        match mode.lower():
            case "read":
                return self.read(file_path=file_path)
            case "write":
                return self.write(
                    file_path=file_path,
                    content=content,
                    mode=write_mode
                )
            case _:
                raise ValueError("mode может быть только `read` или `write`")
