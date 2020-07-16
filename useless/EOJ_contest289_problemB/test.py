from math import inf
from os import listdir
from tqdm import trange

path = r'C:\Users\ccxxx\ecnu\数据结构与算法\Grand Order\test'
files = listdir(path)

x_min = y_min = inf
x_max = y_max = -inf

for idx in trange(len(files)):
    with open(rf'{path}\{files[idx]}') as f:
        m, n = map(int, f.readline().split())
        for _ in range(m):
            name, x, y, key = f.readline().split()
            x_min = min(x_min, int(x))
            y_min = min(y_min, int(y))
            x_max = max(x_max, int(x))
            y_max = max(y_max, int(y))

print(f'{x_min=}')
print(f'{x_max=}')
print(f'{y_min=}')
print(f'{y_max=}')
