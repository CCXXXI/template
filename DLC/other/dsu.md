# 并查集

```cpp
#pragma region Disjoint Set Union

// 朴素的并查集
class dsu {
protected:
    vector<u32> pa_, size_;

    // 路径压缩
    $ find(u32 const& x) -> u32 {
        return pa_[x] == x ? x : pa_[x] = find(pa_[x]);
    }

    // 仅供继承用
    dsu() = default;

public:
    explicit dsu(u32 const& sz) {
        pa_.resize(sz);
        iota(pa_.begin(), pa_.end(), 0);
        size_.resize(sz, 1);
    }

    // 启发式合并
    $ unite(u32 x, u32 y) {
        x = find(x);
        y = find(y);
        if (x != y) {
            if (size_[x] > size_[y]) {
                swap(x, y);
            }
            pa_[x] = y;
            size_[y] += size_[x];
        }
    }

    $ same(u32 const& x, u32 const& y) {
        return find(x) == find(y);
    }

    $ size_of(u32 const& x) {
        return size_[find(x)];
    }
};

// 带删除操作的并查集
class dsu_with_erase : public dsu {
public:
    explicit dsu_with_erase(u32 const& sz) {
        pa_.resize(sz + sz);
        for (u32 i = 0; i < sz; ++i) {
            pa_[i] = pa_[i + sz] = i + sz;
        }
        size_.resize(sz + sz, 1);
    }

    $ erase(u32 const& x) {
        pa_[x] = x;
    }
};

#pragma endregion

```
