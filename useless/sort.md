# 排序

> 对呀对呀！……排序有十二样写法，你知道么？

## 冒泡排序

这种算法能如此知名，可能是历史遗留问题

平均与最坏时间复杂度均为n^2，最好为n，不需要额外空间，稳定

有意避免了随机访问的写法，以便对链表进行排序

尽管如此仍然毫无实用价值

------

```cpp
template <typename It>
$ bubble_sort(It first, It last) {
    for ($ ok = false; !ok; --last) {
        ok = true;
        for ($ cur = first;; ++cur) {
            $ next = cur;
            if (++next == last) {
                break;
            }
            if (*cur > *next) {
                ok = false;
                iter_swap(cur, next);
            }
        }
    }
}

```
