# 线段树

------

```cpp
#pragma region segment tree

// 线段树，点修改、区间查询
template <typename T = int>
class sgt
{
    u32 n_ = 1;
    vector<T> tree_;
    T init_val_;
    function<T(T, T)> func_;

    $ build()
    {
        for ($ i = n_ - 1; i != 0;)
        {
            --i;
            tree_[i] = func_(tree_[i * 2 + 1], tree_[i * 2 + 2]);
        }
    }

public:
    sgt(u32 C& n, T C& init_val, function<T(T, T)> func)
        : init_val_(init_val), func_(move(func))
    {
        while (n_ < n)
        {
            n_ *= 2;
        }
        tree_.resize(n_ * 2 - 1, init_val_);
    }

    sgt(vector<T>&& a, T C& init_val, function<T(T, T)>C& func)
        : sgt(a.size(), init_val, func)
    {
        move(a.begin(), a.end(), tree_.begin() + n_ - 1);
        build();
    }

    sgt(vector<T>C& a, T C& init_val, function<T(T, T)>C& func)
        : sgt(a.size(), init_val, func)
    {
        copy(a.begin(), a.end(), tree_.begin() + n_ - 1);
        build();
    }

    // a[i] = v
    $ set(u32 i, T C& v)
    {
        i += n_ - 1;
        tree_[i] = v;
        while (i != 0)
        {
            i = (i - 1) / 2;
            tree_[i] = func_(tree_[i * 2 + 1], tree_[i * 2 + 2]);
        }
    }

    // 求[i, j)在func意义下的和
    $ query(u32 C& i, u32 C& j)C
    {
        T res = init_val_;
        function<void(u32, u32, u32)> dfs = [&](u32 C& o, u32 C& l, u32 C& r)
        {
            if (r <= i or j <= l)
            {
                return;
            }
            if (i <= l and r <= j)
            {
                res = func_(res, tree_[o]);
                return;
            }
            $ C m = (l + r) / 2;
            dfs(o * 2 + 1, l, m);
            dfs(o * 2 + 2, m, r);
        };
        dfs(0, 0, n_);
        return res;
    }
};

#pragma endregion

```
