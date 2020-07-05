# 排序

> 对呀对呀！……排序有十二样写法，你知道么？

## 冒泡排序

这种算法能如此知名，可能是历史遗留问题

平均与最坏复杂度均为n^2，最好为n，稳定

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

## 选择排序

复杂度在最好与最坏情况下均为n^2，不稳定

------

```cpp
template <typename It>
$ selection_sort(It first, It last) {
    for (; first != last; ++first) {
        iter_swap(first, min_element(first, last));
    }
}

```

## 插入排序

平均与最坏复杂度均为n^2，最好为n，稳定

对于接近有序的、数据量小的数组表现很好

迭代器不能小于`first`，于是写出了如此奇怪的代码

------

```cpp
template <typename It>
$ insertion_sort(It first, It last) {
    for ($ cur = first; ++cur != last;) {
        $ const cur_val = *cur;
        $ pos = cur, pre = cur;
        --pre;
        while (*pre > cur_val) {
            *pos-- = move(*pre);
            if (pre != first) {
                --pre;
            }
            else {
                break;
            }
        }
        *pos = cur_val;
    }
}

```

## 希尔排序

基于插入排序进行了一些优化，把插入排序仅有的优势也优化掉了

------

```cpp
template <typename It, u32 Inc>
$ shell_sort(It first, It last) {
    for ($ cur = first + Inc; cur < last; ++cur) {
        for ($ pre = cur - Inc; *pre > pre[Inc];) {
            iter_swap(pre, pre + Inc);
            if (pre - first >= Inc) {
                pre -= Inc;
            }
        }
    }
}

```

## 归并排序

复杂度在最好与最坏情况下均为nlgn，稳定

常用于外部排序（其实常用的是多路归并）

------

```cpp
template <typename It>
$ merge_sort(It first, It last) -> void {
    $C num = last - first;
    if (num > 1) {
        $C mid = first + num / 2;
        merge_sort(first, mid);
        merge_sort(mid, last);
        inplace_merge(first, mid, last);
    }
}

```

## 快速排序

复杂度平均与最好nlgn，最坏n^2，不稳定

速度很受pivot影响，但是反正也不会真的拿去用，随便取了

------

```cpp
template <typename It>
$ quick_sort(It first, It last) -> void {
    if (first != last) {
        $ const pivot = *(first + (last - first) / 2);
        $C mid1 = partition(first, last, [&]($C e) {
            return e < pivot;
        });
        $C mid2 = partition(mid1, last, [&]($C e) {
            return e <= pivot;
        });
        quick_sort(first, mid1);
        quick_sort(mid2, last);
    }
}

```

## 堆排序

复杂度在最好与最坏情况下均为nlgn，不稳定

缓存不友好，因而常数较大，虽然最坏nlgn但一般慢于快排

------

```cpp
template <typename It>
$ heap_sort(It first, It last){
    make_heap(first, last);
    sort_heap(first, last);
}

```

## 计数排序

非比较排序，因而复杂度可以低于nlgn

需要数据比较密集才有较好表现

复杂度n+k，k为数据取值范围大小

稳定

------

```cpp
template <typename It>
$ counting_sort(It first, It last){
    $C[mi,mx] = minmax_element(first, last);
    $ const min_val = *mi, max_val = *mx;
    $ cnt = vector<typename It::value_type>(max_val - min_val + 1);
    for ($ it = first; it != last; ++it) {
        ++cnt[*it - min_val];
    }
    for ($ val = min_val; val <= max_val; ++val) {
        while (cnt[val - min_val]--) {
            *first++ = val;
        }
    }
}

```

## 桶排序

泛化的计数排序，需要数据分布比较均匀

K取1即为计数排序

------

```cpp
template <typename It, u32 K = 64>
$ bucket_sort(It first, It last){
    $C[mi,mx] = minmax_element(first, last);
    $ const min_val = *mi, max_val = *mx;
    $ cnt = vector<vector<typename It::value_type>>((max_val - min_val) / K + 1);
    for ($ it = first; it != last; ++it) {
        cnt[(*it - min_val) / K].push_back(move(*it));
    }
    for ($$ c : cnt) {
        sort(c.begin(), c.end());
        for ($$ i : c) {
            *first++ = move(i);
        }
    }
}

```

## 基数排序

桶排序变体，每次把基数相同的分在一个桶

对于整数差不多就是上面代码里K取10，然后sort改为递归进行基数排序

所以没有单独的代码

## 猴子排序

由莎士比亚的猴子进行排序

最好复杂度n，平均复杂度(n+1)!，最坏复杂度……

------

```cpp
template <typename It>
$ monkey_sort(It first, It last) {
    $ rd = random_device();
    $ monkey = mt19937(rd());
    while (!is_sorted(first, last)) {
        shuffle(first, last, monkey);
    }
}

```

## multiset排序

凑个数

------

```cpp
template <typename It>
$ multiset_sort(It first, It last) {
    $C tmp = multiset(first, last);
    move(tmp.begin(), tmp.end(), first);
}

```
