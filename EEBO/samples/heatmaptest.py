import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

xedges = [0, 1, 3, 5]
yedges = [0, 2, 3, 4, 6]

x = np.random.normal(2, 1, 100)
y = np.random.normal(1, 1, 100)

print(x)
print(y)

H, xedges, yedges = np.histogram2d(x,y,bins=(xedges, yedges))

print(H)
print(xedges)
print(yedges)