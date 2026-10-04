from dataclasses import dataclass
from sympy import sympify, latex, nsimplify
from sympy.parsing.latex import parse_latex

@dataclass
class Point:
    def __init__(self, x, y):
        self.x = self._parse_coordinate(x)
        self.y = self._parse_coordinate(y)

    def _parse_coordinate(self, val):
        if isinstance(val, str):
            val_stripped = val.strip()
            if val_stripped.startswith('$') and val_stripped.endswith('$'):
                latex_content = val_stripped[1:-1].strip()
                return parse_latex(latex_content, backend='lark')

        # 1. Сначала превращаем в объект SymPy (PyCharm спокоен)
        sympy_val = sympify(val)

        # 2. Если это float, превращаем его в точную рациональную дробь
        if sympy_val.is_Float:
            return nsimplify(sympy_val)

        return sympy_val

    def __repr__(self):
        return f'Point({self.x}, {self.y})'

    def __str__(self):
        return f'({self.x.evalf()}, {self.y.evalf()})'

    def _repr_latex_(self):
        return f"$({latex(self.x)}, {latex(self.y)})$"

    def to_float(self, digits=None):
        """
        Возвращает новую точку с десятичными координатами.
        digits — количество знаков после запятой (опционально).
        """
        # Если digits передан, округляем до этого количества знаков
        new_x = self.x.evalf(digits) if digits else self.x.evalf()
        new_y = self.y.evalf(digits) if digits else self.y.evalf()

        # Создаем и возвращаем новую точку
        return Point(new_x, new_y)