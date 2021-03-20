import numpy as np
import matplotlib.pyplot as plt

y = []
for i in range(10000):
    t = sum([np.random.random() * np.random.randint(1, 100) for _ in range(100)])
    y.append(t)
maxy = max(y)
miny = min(y)
county = []
mid = (maxy - miny) / 100
for i in np.arange(miny, maxy, mid):
    count = ((i < y) & (y < i + mid)).sum()
    county.append(count)

x = [k for k in range(len(county))]
plt.plot(x, county)
plt.show()
