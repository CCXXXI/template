# 踩过的坑

## python

### RecursionError

```py
from sys import setrecursionlimit
setrecursionlimit(10**8)

```

### IO加速

```py
from sys import stdout, stdin

```

## other

* 如果边读入边计算答案，注意提前得到了结果时，不要直接break
* 滚动数组注意清空历史数据
