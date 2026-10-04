import numpy as np
import math
from typing import Optional, Tuple, List
from dataclasses import dataclass

@dataclass
class Point:
    x: float
    y: float


def find_line_equation(p1: Point, p2: Point) -> Tuple[Optional[float], float]:
    """
    Находит коэффициенты k и b для уравнения прямой y = kx + b по двум точкам.
    Возвращает кортеж (k, b).

    Если прямая вертикальная (x1 == x2), возвращает (None, x_value),
    так как уравнение имеет вид x = const.
    """
    # Проверка на совпадение точек, чтобы избежать неопределенности
    if p1.x == p2.x and p1.y == p2.y:
        raise ValueError("Точки p1 и p2 должны быть уникальными для построения прямой.")

    # Случай вертикальной прямой (деление на ноль)
    if p1.x == p2.x:
        # Уравнение прямой выглядит как x = p1.x (k не существует)
        return None, p1.x

    # Формула углового коэффициента: k = (y2 - y1) / (x2 - x1)
    k = (p2.y - p1.y) / (p2.x - p1.x)

    # Формула свободного члена: b = y1 - k * x1
    b = p1.y - k * p1.x

    return k, b

def midpoint(p1: Point, p2: Point) -> Point:
    """Возвращает новую точку, которая является серединой между p1 и p2."""
    x_mid = (p1.x + p2.x) / 2
    y_mid = (p1.y + p2.y) / 2
    return Point(x_mid, y_mid)


def find_perpendicular_line(k: Optional[float], b: float, p: Point) -> Tuple[Optional[float], float]:
    """
    Находит уравнение прямой, перпендикулярной исходной (y = kx + b)
    и проходящей через точку p.

    Принимает:
        k: угловой коэффициент исходной прямой (None, если прямая вертикальная x = b)
        b: свободный член исходной прямой (или значение x для вертикальной прямой)
        p: точка Point, через которую проходит перпендикуляр

    Возвращает:
        Кортеж (k_new, b_new) для уравнения перпендикуляра.
    """
    # 1. Если исходная прямая вертикальная (x = b),
    # то перпендикуляр будет горизонтальным (y = p.y), то есть k_new = 0, b_new = p.y
    if k is None:
        return 0.0, p.y

    # 2. Если исходная прямая горизонтальная (y = b, то есть k == 0),
    # то перпендикуляр будет вертикальным (x = p.x), то есть k_new = None, b_new = p.x
    if k == 0:
        return None, p.x

    # 3. Общий случай: k1 * k2 = -1  =>  k2 = -1 / k1
    k_new = -1 / k

    # Находим свободный член из уравнения y = k_new * x + b_new
    # Подставляем координаты точки p: b_new = y_p - k_new * x_p
    b_new = p.y - k_new * p.x

    return k_new, b_new


def find_line_circle_intersections(
        k: Optional[float], b: float,
        x_c: float, y_c: float, r: float
) -> List[Point]:
    """
    Находит точки пересечения прямой и окружности.

    Прямая задается: k и b (y = kx + b). Если k is None, прямая вертикальная: x = b.
    Окружность задается: x_c, y_c (центр) и r (радиус).

    Возвращает список объектов Point (может содержать 0, 1 или 2 точки).
    """
    if r < 0:
        raise ValueError("Радиус окружности не может быть отрицательным.")

    points = []

    # СЛУЧАЙ 1: Вертикальная прямая x = b
    if k is None:
        x_val = b
        # Подставляем x в уравнение окружности: (b - x_c)^2 + (y - y_c)^2 = r^2
        # (y - y_c)^2 = r^2 - (b - x_c)^2
        discr = r ** 2 - (x_val - x_c) ** 2

        if discr < 0:
            return []  # Прямая проходит мимо окружности
        elif abs(discr) < 1e-9:  # Касание (дискриминант близок к нулю)
            y_val = y_c
            points.append(Point(x_val, y_val))
        else:  # Два пересечения
            y1 = y_c + math.sqrt(discr)
            y2 = y_c - math.sqrt(discr)
            points.append(Point(x_val, y1))
            points.append(Point(x_val, y2))

        return points

    # СЛУЧАЙ 2: Стандартная прямая y = kx + b
    # Подставляем y в уравнение окружности: (x - x_c)^2 + (kx + b - y_c)^2 = r^2
    # Раскрываем скобки и собираем коэффициенты Ax^2 + Bx + C = 0:
    # (x^2 - 2*x*x_c + x_c^2) + (k^2*x^2 + 2*k*x*(b - y_c) + (b - y_c)^2) - r^2 = 0

    A = 1 + k ** 2
    B = -2 * x_c + 2 * k * (b - y_c)
    C = x_c ** 2 + (b - y_c) ** 2 - r ** 2

    # Считаем дискриминант
    D = B ** 2 - 4 * A * C

    if D < -1e-9:
        return []  # Пересечений нет

    if abs(D) < 1e-9:
        # Одна точка касания
        x = -B / (2 * A)
        y = k * x + b
        points.append(Point(x, y))
    else:
        # Две точки пересечения
        x1 = (-B + math.sqrt(D)) / (2 * A)
        y1 = k * x1 + b

        x2 = (-B - math.sqrt(D)) / (2 * A)
        y2 = k * x2 + b

        points.append(Point(x1, y1))
        points.append(Point(x2, y2))

    return points



def find_intersection(
        k1: Optional[float], b1: float,
        k2: Optional[float], b2: float
) -> Optional[Point]:
    """
    Находит точку пересечения двух прямых.
    Прямая 1: задается k1 и b1 (если k1=None, то x = b1)
    Прямая 2: задается k2 и b2 (если k2=None, то x = b2)

    Возвращает:
        Экземпляр Point, если прямые пересекаются.
        None, если прямые параллельны или совпадают (нет единственной точки пересечения).
    """
    # Случай 1: Обе прямые вертикальные (k1 == None и k2 == None)
    if k1 is None and k2 is None:
        # Они либо параллельны (разные x), либо совпадают. Единственной точки нет.
        return None

    # Случай 2: Первая прямая вертикальная (x = b1), а вторая — обычная
    if k1 is None:
        x = b1
        y = k2 * x + b2
        return Point(x, y)

    # Случай 3: Вторая прямая вертикальная (x = b2), а первая — обычная
    if k2 is None:
        x = b2
        y = k1 * x + b1
        return Point(x, y)

    # Случай 4: Обе прямые не вертикальные, но имеют одинаковый угловой коэффициент
    if k1 == k2:
        # Если k одинаковые, они либо параллельны (разные b), либо совпадают (одинаковые b)
        return None

    # Общий случай: классические невертикальные прямые с разными углами наклона
    x = (b2 - b1) / (k1 - k2)
    y = k1 * x + b1

    return Point(x, y)


# a = Point(1, 0)
# b = Point(-1, 0)
# c = Point(0, 2)
#
# m_ac = midpoint(a, c)
# m_bc = midpoint(b, c)
#
# l_ac = find_line_equation(a, c)
# p_ac = find_perpendicular_line(l_ac[0], l_ac[1], m_ac)
#
# l_bc = find_line_equation(b, c)
# p_bc = find_perpendicular_line(l_bc[0], l_bc[1], m_bc)
#
# center = find_intersection(p_ac[0], p_ac[1], p_bc[0], p_bc[1])

okr = (-2, -1, 4)
line = (-1, 1)

print(find_line_circle_intersections(line[0], line[1], okr[0], okr[1], okr[2]))
print(find_line_circle_intersections(None, 0, okr[0], okr[1], okr[2]))
print(find_intersection(-1, 1, None, 0))

v_po = np.array([0, -12])
v_or = np.array([-9, 0])
v_ps = np.array([0, -24])
v_ts = np.array([-9, -12])

print(np.linalg.norm(v_po + v_or + v_ps - v_ts))