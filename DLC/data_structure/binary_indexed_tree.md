# 树状数组

------

```cpp
#pragma region binary indexed tree

$ constexpr low_bit(u32 C& i)
{
    return i & ~i + 1;
}

// 树状数组，点更新、范围查询
template <typename T = int>
class bit
{
    vector<T> tree_; // tree是原始数组a的树状数组

public:
    u32 n; // 有效下标1...n

    explicit bit(u32 C& n_in) : n(n_in)
    {
        tree_.resize(n + 2);
    }

    // a[i] += d
    $ add(u32 i, T C& d)
    {
        for (; i <= n; i += low_bit(i))
        {
            tree_[i] += d;
        }
    }

    // a[1] + ... + a[i]
    $ prefix_sum(u32 i)C
    {
        T res = 0;
        for (; i >= 1; i -= low_bit(i))
        {
            res += tree_[i];
        }
        return res;
    }

    // a[i] + ... + a[j]
    $ sum(u32 C& i, u32 C& j)C
    {
        return prefix_sum(j) - prefix_sum(i - 1);
    }

    // a[i]
    $ operator[](u32 C& i)C
    {
        return sum(i, i);
    }
};

// 树状数组，范围更新、点查询
template <typename T = int>
class bit_kai
{
    bit<T> tree_; // tree是a的差分数组b的树状数组

public:
    explicit bit_kai(u32 C& n) : tree_(n)
    {
    }

    // a[i...j] += d <=> b[i] += d, b[j + 1] -= d
    $ add(u32 C& i, u32 C& j, T C& d)
    {
        tree_.add(i, d);
        tree_.add(j + 1, -d);
    }

    // a[i] += d
    $ add(u32 C& i, T C& d)
    {
        add(i, i, d);
    }

    // a[i] == b[1] + ... + b[i]
    $ operator[](u32 C& i)C
    {
        return tree_.prefix_sum(i);
    }
};

// 树状数组，范围更新、范围查询
template <typename T = int>
class bit_ultimate
{
    vector<T> tree1_; // tree1是b的树状数组
    vector<T> tree2_; // tree2是b*i的树状数组
    u32 n_; // 有效下标1...n

    // a[i...n] += d <=> b[i] += d, bi[i] += d * i
    $ suffix_add(u32 i, T C& d)
    {
        $ di = d * static_cast<T>(i);
        for (; i <= n_; i += low_bit(i))
        {
            tree1_[i] += d;
            tree2_[i] += di;
        }
    }

public:
    explicit bit_ultimate(u32 C& n_in) : n_(n_in)
    {
        tree1_.resize(n_ + 2);
        tree2_.resize(n_ + 2);
    }

    // a[i...j] += d <=> a[i...n] += d, a[(j+1)...n] -= d
    $ add(u32 C& i, u32 C& j, T C& d)
    {
        suffix_add(i, d);
        suffix_add(j + 1, -d);
    }

    // a[i] += d
    $ add(u32 C& i, T C& d)
    {
        add(i, i, d);
    }

    // a[1] + ... + a[i]
    $ prefix_sum(u32 i)C
    {
        T res = 0;
        $ x = i + 1;
        for (; i >= 1; i -= low_bit(i))
        {
            res += x * tree1_[i] - tree2_[i];
        }
        return res;
    }

    // a[i] + ... + a[j]
    $ sum(u32 C& i, u32 C& j)C
    {
        return prefix_sum(j) - prefix_sum(i - 1);
    }

    // a[i]
    $ operator[](u32 C& i)C
    {
        return sum(i, i);
    }
};

#pragma endregion

```
