from sympy import symbols, sympify, nsimplify, latex, Expr
from sympy.parsing.latex import parse_latex


# Предполагаем, что класс Point импортируется или объявлен выше
# from point import Point

class LinearFunction:
    def __init__(self, k, b):
        """Инициализация функции y = kx + b"""
        self.k: Expr = self._parse_coefficient(k)
        self.b: Expr = self._parse_coefficient(b)
        self.x = symbols('x')

    def _parse_coefficient(self, val) -> Expr:
        """Парсинг коэффициентов (поддерживает int, float, str, $, SymPy)"""
        if isinstance(val, str):
            val_stripped = val.strip()
            if val_stripped.startswith('$') and val_stripped.endswith('$'):
                latex_content = val_stripped[1:-1].strip()
                # Если antlr4 починен, оставляем без backend. Если нет — backend='lark'
                return parse_latex(latex_content)

        sympy_val = sympify(val)
        if sympy_val.is_Float:
            return nsimplify(sympy_val)

        return sympy_val

    @classmethod
    def from_two_points(cls, p1: 'Point', p2: 'Point') -> 'LinearFunction':
        """Статический метод (фабрика) для создания функции по двум точкам"""
        if p1.x == p2.x:
            raise ValueError("Через две точки с одинаковым X нельзя провести функцию вида y = kx + b")

        # k = (y2 - y1) / (x2 - x1)
        k = (p2.y - p1.y) / (p2.x - p1.x)
        # b = y1 - k * x1
        b = p1.y - k * p1.x
        return cls(k, b)

    def expression(self) -> Expr:
        """Возвращает чистое SymPy выражение для функции (kx + b) с учетом знаков"""
        return self.k * self.x + self.b

    def __call__(self, x_val) -> Expr:
        """Позволяет вызывать функцию: f(5) или f(Point.x)"""
        # Если передали объект Point, берем его координату X
        if hasattr(x_val, 'x'):
            x_parsed = x_val.x
        else:
            x_parsed = self._parse_coefficient(x_val)
        return self.expression().subs(self.x, x_parsed)

    def __repr__(self):
        return f"LinearFunction(k={self.k}, b={self.b})"

    def __str__(self):
        return f"y = {self.expression()}"

    def _repr_latex_(self):
        """Красивый вывод уравнения прямой в Jupyter"""
        return f"$y = {latex(self.expression())}$"

    def to_float(self, digits=None) -> 'LinearFunction':
        """Возвращает новую функцию с десятичными (float) коэффициентами"""
        new_k = self.k.evalf(digits) if digits else self.k.evalf()
        new_b = self.b.evalf(digits) if digits else self.b.evalf()
        return LinearFunction(new_k, new_b)
