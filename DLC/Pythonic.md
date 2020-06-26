# 非正式内容

出于个人喜好添加一些无关紧要的语法糖与美化

若使用此模板，应删去（或注释掉）[基础模板](../base/README.md)中的`ccxxxi()`函数

------

```cpp
#pragma region Pythonic

#ifndef ONLINE_JUDGE
// 给单调的黑框框加点色彩
$C input_style = "\033[34;1m"; // 蓝色加亮
$C print_style = "\033[m"; // 默认白色字
$C debug_style = "\033[32;1m"; // 绿色加亮
#define DBG(x) cout << debug_style << #x << ": " << (x) << "\n" << input_style
#else
#define DBG(x)
#endif

$ ccxxxi() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
#ifndef ONLINE_JUDGE
    cout << input_style;
#endif
}

// cout << pair
template <typename K, typename V>
$ operator<<(ostream& o, pair<K, V> const& p) -> auto& {
    return o << p.first << " " << p.second << " ";
}

// cout << vector
template <typename E>
$ operator<<(ostream& o, vector<E> const& v) -> auto& {
    for ($$ i : v) {
        o << i << " ";
    }
    return o;
}

// py风格print单参数特化
template <typename T>
$ print(T const& a) {
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
$ print(T const& a, Ts const&... args) {
#ifndef ONLINE_JUDGE
    cout << print_style;
#endif
    cout << a << " ";
    print(args...);
}

#pragma endregion

$ main() -> int {
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