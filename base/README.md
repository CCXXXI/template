# 基础模板

[stdc++.h](./stdc++.h)为了在vs下正常工作而进行了修改，顺带一提原版最新版在[这里](https://raw.githubusercontent.com/gcc-mirror/gcc/master/libstdc%2B%2B-v3/include/precompiled/stdc%2B%2B.h)

<!-- 以下代码应与[此处](./Pythonic.md)同时修改 -->

------

```cpp
#pragma region base

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

$ ccxxxi()
{
#ifdef ONLINE_JUDGE
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
#endif
}

#pragma endregion

$ main() -> int
{
    ccxxxi();

    cout << "Hello world!\n";
}

```
