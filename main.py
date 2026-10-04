import numpy as np
import math
from typing import Optional, Tuple, List
from dataclasses import dataclass

from sympy import sympify, latex

from src.point import Point










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