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

// 线段树，区间set&add、sum&min&max
template <u32 N>
class sgt_large
{
    u32 n_;

    using v_t = vector<i64>;
    i64 C no_ = INT64_MAX;
    v_t set_ = v_t(N * 4, no_),
        add_ = v_t(N * 4, 0),
        sum_ = v_t(N * 4, 0),
        min_ = v_t(N * 4, 0),
        max_ = v_t(N * 4, 0);

    // 以子节点更新o
    $ maintain(u32 C& o, u32 C& l, u32 C& r)
    {
        $ C num = r - l;
        if (num == 1) // 叶子节点
        {
            sum_[o] = min_[o] = max_[o] = 0;
        }
        else
        {
            $ C lc = o * 2 + 1, rc = o * 2 + 2;
            sum_[o] = sum_[lc] + sum_[rc];
            min_[o] = min(min_[lc], min_[rc]);
            max_[o] = max(max_[lc], max_[rc]);
        }
        if (set_[o] != no_)
        {
            sum_[o] = set_[o] * num;
            min_[o] = max_[o] = set_[o];
        }
        if (add_[o] != 0)
        {
            sum_[o] += add_[o] * num;
            min_[o] += add_[o];
            max_[o] += add_[o];
        }
    }

    // 下传标记
    $ down(u32 C& o)
    {
        $ C lc = o * 2 + 1, rc = o * 2 + 2;
        if (set_[o] != no_)
        {
            set_[lc] = set_[rc] = set_[o];
            add_[lc] = add_[rc] = 0;
            set_[o] = no_;
        }
        if (add_[o] != 0)
        {
            add_[lc] += add_[o];
            add_[rc] += add_[o];
            add_[o] = 0;
        }
    }

    template <bool Set>
    $ set_or_add(u32 C& i, u32 C& j, i64 C& v)
    {
        function<void(u32, u32, u32)> dfs = [&](u32 C& o, u32 C& l, u32 C& r)
        {
            if (r <= i or j <= l)
            {
                maintain(o, l, r);
                return;
            }
            if (i <= l and r <= j)
            {
                if constexpr (Set)
                {
                    set_[o] = v;
                    add_[o] = 0;
                }
                else
                {
                    add_[o] += v;
                }
            }
            else
            {
                down(o);
                $ C m = (l + r) / 2;
                dfs(o * 2 + 1, l, m);
                dfs(o * 2 + 2, m, r);
            }
            maintain(o, l, r);
        };
        dfs(0, 0, n_);
    }

public:
    explicit sgt_large(u32 C& n): n_(n)
    {
    }

    explicit sgt_large(v_t C& a): n_(a.size())
    {
        function<void(u32, u32, u32)> dfs = [&](u32 C& o, u32 C& l, u32 C& r)
        {
            if (r - l == 1)
            {
                add_[o] = a[l];
            }
            else
            {
                $ C m = (l + r) / 2;
                dfs(o * 2 + 1, l, m);
                dfs(o * 2 + 2, m, r);
            }
            maintain(o, l, r);
        };
        dfs(0, 0, n_);
    }

    // a[i...(j-1)] = v
    $ set(u32 C& i, u32 C& j, i64 C& v)
    {
        set_or_add<true>(i, j, v);
    }

    // a[i...(j-1)] += v
    $ add(u32 C& i, u32 C& j, i64 C& v)
    {
        set_or_add<false>(i, j, v);
    }

private:
    struct smm
    {
        i64 sum, min, max;
    };

public:
    // 求[i, j)的sum&min&max
    $ query(u32 C& i, u32 C& j)C
    {
        $ res = smm{0,INT64_MAX,INT64_MIN};
        function<void(u32, u32, u32, i64)> dfs = [&](u32 C& o, u32 C& l, u32 C& r, i64 C& add_val)
        {
            if (r <= i or j <= l)
            {
                return;
            }
            if (set_[o] != no_)
            {
                $ C tmp = set_[o] + add_val + add_[o];
                $ C num = min(r, j) - max(l, i);
                res.sum += tmp * num;
                res.min = min(res.min, tmp);
                res.max = max(res.max, tmp);
            }
            else if (i <= l and r <= j)
            {
                res.sum += sum_[o] + add_val * (r - l);
                res.min = min(res.min, min_[o] + add_val);
                res.max = max(res.max, max_[o] + add_val);
            }
            else
            {
                $ C m = (l + r) / 2;
                dfs(o * 2 + 1, l, m, add_val + add_[o]);
                dfs(o * 2 + 2, m, r, add_val + add_[o]);
            }
        };
        dfs(0, 0, n_, 0);
        return res;
    }
};

#pragma endregion

```
