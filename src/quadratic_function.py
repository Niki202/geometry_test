from sympy import symbols, sympify, nsimplify, latex, Expr, solve
from sympy.parsing.latex import parse_latex
from src.point import Point


class QuadraticFunction:
    def __init__(self, a, b, c):
        """Инициализация функции y = ax^2 + bx + c"""
        self.a: Expr = self._parse_coefficient(a)
        self.b: Expr = self._parse_coefficient(b)
        self.c: Expr = self._parse_coefficient(c)

        if self.a == 0:
            raise ValueError("Коэффициент 'a' не может быть равен 0 для квадратичной функции.")

        self.x = symbols('x')

    def _parse_coefficient(self, val) -> Expr:
        """Парсинг коэффициентов (поддерживает int, float, str, $, SymPy)"""
        if isinstance(val, str):
            val_stripped = val.strip()
            if val_stripped.startswith('$') and val_stripped.endswith('$'):
                latex_content = val_stripped[1:-1].strip()
                return parse_latex(latex_content)

        sympy_val = sympify(val)
        if sympy_val.is_Float:
            return nsimplify(sympy_val)

        return sympy_val

    @classmethod
    def from_three_points(cls, p1: 'Point', p2: 'Point', p3: 'Point') -> 'QuadraticFunction':
        """Фабрика: строит единственную параболу, проходящую через 3 заданные точки"""
        from sympy import solve

        # Задаем символы для поиска коэффициентов
        a, b, c = symbols('a b c')

        # Составляем систему уравнений: a*x^2 + b*x + c = y для каждой точки
        eq1 = a * p1.x ** 2 + b * p1.x + c - p1.y
        eq2 = a * p2.x ** 2 + b * p2.x + c - p2.y
        eq3 = a * p3.x ** 2 + b * p3.x + c - p3.y

        # Решаем систему
        solution = solve([eq1, eq2, eq3], (a, b, c))

        if not solution or solution[a] == 0:
            raise ValueError("Через эти три точки нельзя провести квадратичную функцию.")

        return cls(solution[a], solution[b], solution[c])

    def expression(self) -> Expr:
        """Возвращает чистое SymPy выражение для функции (ax^2 + bx + c)"""
        return self.a * self.x ** 2 + self.b * self.x + self.c

    def vertex(self) -> 'Point':
        """Возвращает координаты вершины параболы (Point) в точном аналитическом виде"""
        from sympy import Rational
        # x_v = -b / (2a)
        x_v = -self.b / (2 * self.a)
        # y_v = f(x_v)
        y_v = self.expression().subs(self.x, x_v)
        return Point(x_v, y_v)

    def roots(self) -> list:
        """Возвращает список точных корней (точки пересечения с осью X, где y=0)"""
        # Находим только вещественные корни уравнения ax^2 + bx + c = 0
        return solve(self.expression(), self.x)

    def __call__(self, x_val) -> Expr:
        """Позволяет вызывать функцию: f(5) или f(Point.x)"""
        if hasattr(x_val, 'x'):
            x_parsed = x_val.x
        else:
            x_parsed = self._parse_coefficient(x_val)
        return self.expression().subs(self.x, x_parsed)

    def __repr__(self):
        return f"QuadraticFunction(a={self.a}, b={self.b}, c={self.c})"

    def __str__(self):
        return f"y = {self.expression()}"

    def _repr_latex_(self):
        """Красивый вывод параболы в Jupyter с автоматическим упорядочиванием степеней"""
        return f"$y = {latex(self.expression())}$"

    def to_float(self, digits=None) -> 'QuadraticFunction':
        """Возвращает новую функцию с десятичными (float) коэффициентами"""
        new_a = self.a.evalf(digits) if digits else self.a.evalf()
        new_b = self.b.evalf(digits) if digits else self.b.evalf()
        new_c = self.c.evalf(digits) if digits else self.c.evalf()
        return QuadraticFunction(new_a, new_b, new_c)
