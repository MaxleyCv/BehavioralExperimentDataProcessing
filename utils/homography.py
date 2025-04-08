import math

import numpy as np

homogenize = lambda x: np.array([*x, 1])
dehomogenize_2d = lambda x: np.array([x[0]/x[2], x[1]/x[2]])
eucl_dist = lambda x, y: math.sqrt((x[0] - y[0]) ** 2 + (x[1] - y[1]) ** 2)
