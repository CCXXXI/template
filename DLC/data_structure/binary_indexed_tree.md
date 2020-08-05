# 树状数组

------

```cpp
#pragma region binary indexed tree

// 树状数组，点更新、范围查询
template <typename T = int>
class bit
{
    vector<T> tree_; // tree是对应于原始数组a的线段树
    u32 n_; // 有效下标1...n

    $ static low_bit(u32 C& i)
    {
        return i & ~i + 1;
    }

    // a[1] + ... + a[i]
    $ prefix_sum(u32 i)
    {
        T res = 0;
        for (; i >= 1; i -= low_bit(i))
        {
            res += tree_[i];
        }
        return res;
    }

public:
    explicit bit(u32 C& n) : n_(n)
    {
        tree_.resize(n_ + 1);
    }

    // a[i] += k
    $ add(u32 i, T C& k)
    {
        for (; i <= n_; i += low_bit(i))
        {
            tree_[i] += k;
        }
    }

    // a[i] + ... + a[j]
    $ sum(u32 C& i, u32 C& j)
    {
        return prefix_sum(j) - prefix_sum(i - 1);
    }
};

#pragma endregion

```
