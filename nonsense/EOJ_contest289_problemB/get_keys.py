from os import listdir
from tqdm import trange

path = r'C:\Users\ccxxx\ecnu\数据结构与算法\Grand Order\test'
files = listdir(path)

all_keys = set()

for idx in trange(len(files)):
    with open(rf'{path}\{files[idx]}') as f:
        m, n = map(int, f.readline().split())
        for _ in range(m):
            name, x, y, key = f.readline().split()
            all_keys.add(key)

with open('all_keys.txt', 'w') as f:
    for key in all_keys:
        f.write(f'{key}\n')
