# 字符串

------

```cpp
#pragma region graph

// Z函数
$ z_func(string C& s)
{
    $C n = s.length();
    $ z = vector<u32>(n);
    for (u32 i = 1, l = 0, r = 0; i != n; ++i)
    {
        if (i <= r)
        {
            z[i] = min(r - i + 1, z[i - l]);
        }
        while (i + z[i] < n and s[z[i]] == s[i + z[i]])
        {
            ++z[i];
        }
        if (i + z[i] - 1 > r)
        {
            l = i;
            r = i + z[i] - 1;
        }
    }
    return z;
}

#pragma endregion

```
