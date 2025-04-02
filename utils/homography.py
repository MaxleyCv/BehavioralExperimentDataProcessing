import numpy as np

homogenize = lambda x: np.array([*x, 1])
dehomogenize_2d = lambda x: np.array([x[0]/x[2], x[1]/x[2]])
