from sympy import symbols, sympify, nsimplify, latex, Expr, sqrt
from sympy.parsing.latex import parse_latex
from src.point import Point

class Circle:
    def __init__(self, center: 'Point', radius):
        """Инициализация окружности через центр (Point) и радиус (R)"""
        if not hasattr(center, 'x') or not hasattr(center, 'y'):
            raise TypeError("Аргумент center должен быть экземпляром класса Point")

        self.center: 'Point' = center
        self.r: Expr = self._parse_value(radius)
        self.x, self.y = symbols('x y')

    def _parse_value(self, val) -> Expr:
        """Парсинг радиуса (поддерживает int, float, str, $, SymPy)"""
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
    def from_center_and_point(cls, center: 'Point', point: 'Point') -> 'Circle':
        """Фабрика: создает окружность по центру и точке, лежащей на ней"""
        # R = sqrt((x - x0)^2 + (y - y0)^2)
        radius = sqrt((point.x - center.x) ** 2 + (point.y - center.y) ** 2)
        return cls(center, radius)

    def equation(self) -> Expr:
        """Возвращает чистое SymPy выражение для уравнения окружности (равное R^2)"""
        return (self.x - self.center.x) ** 2 + (self.y - self.center.y) ** 2

    def contains(self, point: 'Point') -> bool:
        """Проверяет, лежит ли точка строго на окружности"""
        # Проверяем, выполняется ли равенство (x-x0)^2 + (y-y0)^2 == R^2
        return self.equation().subs({self.x: point.x, self.y: point.y}) == self.r ** 2

    def __repr__(self):
        return f"Circle(center={self.center}, radius={self.r})"

    def __str__(self):
        return f"({self.x} - {self.center.x})**2 + ({self.y - self.center.y})**2 = {self.r}**2"

    def _repr_latex_(self):
        """Красивый вывод канонического уравнения окружности в Jupyter"""
        # Считаем R^2 для правой части уравнения
        r_squared_latex = latex(self.r ** 2)

        # Формируем скобки с учетом знаков координат центра
        x_part = f"x - {latex(self.center.x)}" if self.center.x >= 0 else f"x + {latex(-self.center.x)}"
        y_part = f"y - {latex(self.center.y)}" if self.center.y >= 0 else f"y + {latex(-self.center.y)}"

        # Если координаты равны 0, убираем лишние скобки
        x_str = "x^2" if self.center.x == 0 else f"\\left({x_part}\\right)^2"
        y_str = "y^2" if self.center.y == 0 else f"\\left({y_part}\\right)^2"

        return f"${x_str} + {y_str} = {r_squared_latex}$"

    def to_float(self, digits=None) -> 'Circle':
        """Возвращает новую окружность с десятичными (float) координатами и радиусом"""
        new_center = self.center.to_float(digits)
        new_r = self.r.evalf(digits) if digits else self.r.evalf()
        return Circle(new_center, new_r)
