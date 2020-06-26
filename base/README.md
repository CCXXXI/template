# 基础模板

[stdc++.h](./stdc++.h)为了在vs下正常工作而进行了修改，顺带一提原版最新版在[这里](https://raw.githubusercontent.com/gcc-mirror/gcc/master/libstdc%2B%2B-v3/include/precompiled/stdc%2B%2B.h)

能拆分的模板已经尽量拆分了出去，剩下的是过于通用必须保留的部分

------

```cpp
#pragma region base

#include "bits/stdc++.h"

using namespace std;

using i64 = int64_t;
using u64 = uint64_t;
using i32 = int32_t;
using u32 = uint32_t;

#define $ auto
#define $$ auto&&
#define $C auto const&

$C inf = 0x3f3f3f3f;

auto ccxxxi() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
}

#pragma endregion

auto main() -> int {
    ccxxxi();
    cout << "Hello world!\n";
}

```