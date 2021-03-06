# 多加点糖

替换[基础模板](./README.md)

<!-- 以下代码应与[此处](./README.md)同时修改 -->

------

```cpp
#pragma region Pythonic

#include "bits/stdc++.h"

using namespace std;

using i64 = int64_t;
using u64 = uint64_t;
using i32 = int32_t;
using u32 = uint32_t;
using i16 = int16_t;
using u16 = uint16_t;
using i8 = int8_t;
using u8 = uint8_t;

#define $ auto
#define $$ auto&&
#define $C auto const&
#define C const

$ constexpr inf = 0x3f3f3f3f;

#ifndef ONLINE_JUDGE
// 给单调的黑框框加点色彩
$ constexpr input_style = "\033[34;1m"; // 蓝色加亮
$ constexpr print_style = "\033[m"; // 默认白色字
$ constexpr debug_style = "\033[32;1m"; // 绿色加亮
#define DBG(x) cout << debug_style << #x << ": " << (x) << "\n" << input_style
#else
#define DBG(x)
#endif

$ ccxxxi()
{
#ifdef ONLINE_JUDGE
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
#else
    cout << input_style;
#endif
}

// cout << pair
template <typename K, typename V>
$ operator<<(ostream& o, pair<K, V> C& p) -> auto&
{
    return o << p.first << " " << p.second << " ";
}

// cout << vector
template <typename E>
$ operator<<(ostream& o, vector<E> C& v) -> auto&
{
    for ($$ i : v)
    {
        o << i << " ";
    }
    return o;
}

// cout << array
template <typename T, u32 N>
$ operator<<(ostream& o, array<T, N> C& arr) -> auto&
{
    for ($$ i : arr)
    {
        o << i << " ";
    }
    return o;
}

// py风格print单参数特化
template <typename T>
$ print(T C& a)
{
#ifndef ONLINE_JUDGE
    cout << print_style;
#endif
    cout << a << "\n";
#ifndef ONLINE_JUDGE
    cout << input_style;
#endif
}

// py风格print，多参数，空格分隔，尾随换行
template <typename T, typename... Ts>
$ print(T C& a, Ts C&... args)
{
#ifndef ONLINE_JUDGE
    cout << print_style;
#endif
    cout << a << " ";
    print(args...);
}

#pragma endregion

$ main() -> int
{
    ccxxxi();

    DBG(1 + 1);

    $C p = pair{"ans", 42};
    $C v = vector{2, 3, 1};
    $C hello = "Hello";
    $C world = "world!";

    print(p, v);
    print(hello, world);
}

```
