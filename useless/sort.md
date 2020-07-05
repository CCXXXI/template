# 排序

> 对呀对呀！……排序有十二样写法，你知道么？

[TOC]

## test

```cpp
$ constexpr sqrt_int(u32 const& n) {
    u32 x = 1;
    $ decreased = false;
    while (true) {
        $C nx = (x + n / x) / 2;
        if (x == nx or nx > x and decreased) {
            break;
        }
        decreased = nx < x;
        x = nx;
    }
    return x;
}

```
