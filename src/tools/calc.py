from ..models import BaseTool

from re import sub, compile
from typing import Dict, Any


class CalcTool(BaseTool):
    def __init__(self):
        self.VALID_CHARS = compile(r'^[0-9.+\-*/%()\s]+$')
        
        self.PARENTHESES = compile(r'\(([^()]+)\)')
        
        self.POW_OP = compile(r'(-?\d+\.?\d*)\s*\*\*\s*(-?\d+\.?\d*)')

        self.FLOOR_DIV_OP = compile(r'(-?\d+\.?\d*)\s*//\s*(-?\d+\.?\d*)')
        
        self.MULT_DIV_MOD_OP = compile(r'(-?\d+\.?\d*)\s*([*/%])\s*(-?\d+\.?\d*)')
        self.ADD_SUB_OP = compile(r'(-?\d+\.?\d*)\s*([+-])\s*(-?\d+\.?\d*)')

    def _calculate_simple(self, expr: str) -> str:        
        while True:
            match = self.POW_OP.search(expr)
            if not match:
                break
            left, right = match.group(1), match.group(2)
            res = float(left) ** float(right)
            expr = expr.replace(match.group(0), str(res), 1)

        while True:
            match = self.FLOOR_DIV_OP.search(expr)
            if not match:
                break
            left, right = match.group(1), match.group(2)
            if float(right) == 0.0:
                raise ZeroDivisionError("деление на ноль")
            res = float(left) // float(right)
            expr = expr.replace(match.group(0), str(res), 1)

        while True:
            match = self.MULT_DIV_MOD_OP.search(expr)
            if not match:
                break
            left, op, right = match.group(1), match.group(2), match.group(3)
            
            if op == '*':
                res = float(left) * float(right)
            elif op == '/':
                if float(right) == 0.0:
                    raise ZeroDivisionError
                res = float(left) / float(right)
            elif op == '%':
                if float(right) == 0.0:
                    raise ZeroDivisionError
                res = float(left) % float(right)
                
            expr = expr.replace(match.group(0), str(res), 1)

        expr = expr.replace('+-', '-').replace('--', '+')

        while True:
            match = self.ADD_SUB_OP.search(expr)
            if not match:
                break
            left, op, right = match.group(1), match.group(2), match.group(3)
            res = float(left) + float(right) if op == '+' else float(left) - float(right)
            expr = expr.replace(match.group(0), str(res), 1)

        return expr

    async def __call__(self, expression: str) -> Dict[str, Any]:
        """
        Вычисляет математическое выражение используя регулярные выражения

        :param expression: Строка с выражением

        :returns Dict[str, Any]: вернет {"result": value}
        """
        clean_expr = expression.strip()
        
        try:
            if not self.VALID_CHARS.match(clean_expr):
                raise ValueError("Выражение содержит недопустимые символы")
            
            working_expr = sub(r'\s+', '', clean_expr)

            while True:
                match = self.PARENTHESES.search(working_expr)
                if not match:
                    break
                sub_res = self._calculate_simple(match.group(1))
                working_expr = working_expr.replace(match.group(0), sub_res, 1)

            final_result = float(self._calculate_simple(working_expr))
            
            if final_result.is_integer():
                result_str = str(int(final_result))
            else:
                result_str = str(round(final_result, 6))

        
            return {
                "expression": clean_expr,
                "result": result_str,
                "status": "success"
            }
                
        except Exception as e:
            return {"result": f"Ошибка вычисления: {str(e)}"}
