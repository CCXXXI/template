# 图

包括并查集

------

```cpp
#pragma region graph

// 朴素的并查集
class dsu {
protected:
    vector<u32> pa_, size_;

    // 路径压缩
    $ find(u32 C& x) -> u32 {
        return pa_[x] == x ? x : pa_[x] = find(pa_[x]);
    }

    // 仅供继承用
    dsu() = default;

public:
    explicit dsu(u32 C& sz) {
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

    $ same(u32 C& x, u32 C& y) {
        return find(x) == find(y);
    }

    $ size_of(u32 C& x) {
        return size_[find(x)];
    }
};

// 带删除操作的并查集
class dsu_with_erase : public dsu {
public:
    explicit dsu_with_erase(u32 C& sz) {
        pa_.resize(sz + sz);
        for (u32 i = 0; i < sz; ++i) {
            pa_[i] = pa_[i + sz] = i + sz;
        }
        size_.resize(sz + sz, 1);
    }

    $ erase(u32 C& x) {
        pa_[x] = x;
    }
};

// 带边权的图，存储为邻接表
template <typename Cost = int, Cost Inf = inf>
class graph_with_cost {
    class edge {
    public:
        u32 to;
        Cost cost;
    };

public:
    vector<vector<edge>> g;
    vector<vector<Cost>> mutable dis;
    vector<vector<u32>> mutable pre;
    u32 sz;

    explicit graph_with_cost(u32 C& sz_in) : sz(sz_in) {
        g.resize(sz + 1);
        dis.resize(sz + 1);
        pre.resize(sz);

        g[sz].reserve(sz);
        for (u32 i = 0; i != sz; ++i) {
            g[sz].push_back(edge{i, 0});
        }
    }

    // 添加u到v，权值为cost的单向边
    $ add(u32 C& u, u32 C& v, Cost C& cost) {
        g[u].push_back(edge{v, cost});
    }

    // 添加uv之间，权值为cost的双向边
    $ add2(u32 C& u, u32 C& v, Cost C& cost) {
        add(u, v, cost);
        add(v, u, cost);
    }

    // 检查是否为二分图，即无奇环
    $ binary_check()C {
        vector<i8> color(sz);
        function<bool(u32, i8)> dfs = [&](u32 C& v, i8 C& c) {
            color[v] = c;
            for ($C e : g[v]) {
                $C u = e.to;
                if (color[u] == c) {
                    return false;
                }
                if (color[u] == 0 and !dfs(u, -c)) {
                    return false;
                }
            }
            return true;
        };
        for (u32 i = 0; i != sz; ++i) {
            if (color[i] == 0) {
                if (!dfs(i, 1)) {
                    return false;
                }
            }
        }
        return true;
    }

private:
    // 以u到v的边e更新dis[start][v]
    template <bool Path = false>
    $ relax(u32 C& start, u32 C& u, edge C& e) C {
        if (dis[start][u] == Inf) {
            return false;
        }
        $C tmp = dis[start][u] + e.cost;
        if (tmp < dis[start][e.to]) {
            dis[start][e.to] = tmp;
            if constexpr (Path) {
                pre[start][e.to] = u;
            }
            return true;
        }
        return false;
    }

public:
    // 求有负权时的单源最短路，基于Bellman-Ford算法，队列优化，O(nm)
    template <bool Path = false>
    $ dis_bf(u32 C& start) C {
        dis[start].resize(sz, Inf);
        dis[start][start] = 0;
        $ que = queue<u32>{};
        que.push(start);
        $ in_que = vector<bool>(sz);
        if constexpr (Path) {
            pre[start].resize(sz, Inf);
        }
        while (!que.empty()) {
            $ C u = que.front();
            que.pop();
            in_que[u] = false;
            for ($C e : g[u]) {
                if (relax<Path>(start, u, e) and !in_que[e.to]) {
                    que.push(e.to);
                    in_que[e.to] = true;
                }
            }
        }
    }

    // 检查是否存在负环，基于Bellman-Ford算法
    $ nl_check()C {
        dis[sz].resize(sz + 1, Inf);
        dis[sz][sz] = 0;
        $ que = queue<u32>{};
        que.push(sz);
        $ in_que = vector<bool>(sz + 1);
        $ upd_tm = vector<u32>(sz, 0);
        while (!que.empty()) {
            $ C u = que.front();
            que.pop();
            in_que[u] = false;
            for ($C e : g[u]) {
                if (relax(sz, u, e) and !in_que[e.to]) {
                    if (++upd_tm[e.to] == sz) {
                        return true;
                    }
                    que.push(e.to);
                    in_que[e.to] = true;
                }
            }
        }
        return false;
    }

    // 求无负权时的单源最短路，基于Dijkstra算法，O(mlgm)
    template <bool Path = false>
    $ dis_dij(u32 C& start) C {
        dis[start].resize(sz, Inf);
        dis[start][start] = 0;
        using p_t = pair<Cost, u32>;
        $ que = priority_queue<p_t, vector<p_t>, greater<>>{};
        que.emplace(Cost(), start);
        if constexpr (Path) {
            pre[start].resize(sz, Inf);
        }
        while (!que.empty()) {
            $ C p = que.top();
            que.pop();
            $ C u = p.second;
            if (dis[start][u] < p.first) {
                continue;
            }
            for ($$ e : g[u]) {
                if (relax<Path>(start, u, e)) {
                    que.emplace(dis[start][e.to], e.to);
                }
            }
        }
    }

    // 求全源最短路，基于Floyd–Warshall算法，O(n^3)
    template <bool Path = false>
    $ dis_fw()C {
        for (u32 i = 0; i != sz; ++i) {
            dis[i].resize(sz, Inf);
            if constexpr (Path) {
                pre[i].resize(sz, Inf);
            }
            for ($C e : g[i]) {
                dis[i][e.to] = e.cost;
                if constexpr (Path) {
                    pre[i][e.to] = i;
                }
            }
            dis[i][i] = 0;
        }
        for (u32 k = 0; k != sz; ++k) {
            for (u32 i = 0; i != sz; ++i) {
                for (u32 j = 0; j != sz; ++j) {
                    $C tmp = dis[i][k] + dis[k][j];
                    if (tmp < dis[i][j]) {
                        dis[i][j] = tmp;
                        if constexpr (Path) {
                            pre[i][j] = k;
                        }
                    }
                }
            }
        }
    }

    // 路径还原，需先求dis[u][v]且指定Path=true
    $ get_path(u32 C& u, u32 v) C {
        $ ret = vector<u32>{};
        for (; v != inf; v = pre[u][v]) {
            ret.push_back(v);
        }
        reverse(ret.begin(), ret.end());
        return ret;
    }
};

// 带边权的图，直接存边，用于求最小生成树
template <typename Cost = int>
class graph_with_cost_mst {
    class edge {
    public:
        u32 u, v;
        Cost cost;

        $ operator<(edge C& e) C {
            return this->cost < e.cost;
        }
    };

    vector<edge> es_;
    u32 sz_;

public:
    // 以顶点数初始化
    explicit graph_with_cost_mst(u32 C& sz_in) : sz_(sz_in) {
    }

    // 添加uv之间，权值为cost的双向边
    $ add(u32 C& u, u32 C& v, Cost C& cost) {
        es_.push_back(edge{u, v, cost});
    }

    // 最小生成树，基于Kruskal算法
    $ mst() {
        sort(es_.begin(), es_.end());
        dsu dsu(sz_);
        Cost ret = 0;
        for ($C e : es_) {
            if (!dsu.same(e.u, e.v)) {
                dsu.unite(e.u, e.v);
                ret += e.cost;
            }
        }
        return ret;
    }
};

#pragma endregion

```
