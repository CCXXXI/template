# 整数平方根

牛顿法，比`std::sqrt`之后再取整大概会快一点点

------

```cpp
$ constexpr sqrt_int(u32 C& n)
{
    u32 x = 1;
    $ decreased = false;
    while (true)
    {
        $C nx = (x + n / x) / 2;
        if (x == nx or nx > x and decreased)
        {
            break;
        }
        decreased = nx < x;
        x = nx;
    }
    return x;
}

```
