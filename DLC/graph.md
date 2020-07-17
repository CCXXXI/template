# 图

```cpp
#pragma region graph

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
    u32 sz;

    explicit graph_with_cost(u32 C& sz_in) : sz(sz_in) {
        g.resize(sz);
        dis.resize(sz);
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
    $ relax(u32 C& start, u32 C& u, edge C& e)C {
        $C tmp = dis[start][u] + e.cost;
        if (tmp < dis[start][e.to]) {
            dis[start][e.to] = tmp;
            return true;
        }
        return false;
    }

public:
    // Bellman-Ford算法，队列优化，仅用于有负权时的单源最短路
    $ bf(u32 C& start)C {
        dis[start].resize(sz, Inf);
        dis[start][start] = 0;
        $ que = queue<u32>{};
        que.push(start);
        $ in_que = vector<bool>(sz);
        while (!que.empty()) {
            $ C u = que.front();
            que.pop();
            in_que[u] = false;
            for ($C e : g[u]) {
                if (relax(start, u, e) and !in_que[e.to]) {
                    que.push(e.to);
                    in_que[e.to] = true;
                }
            }
        }
    }

    // Dijkstra算法，用于无负权时的单源最短路
    $ dij(u32 C& start)C {
        dis[start].resize(sz, Inf);
        dis[start][start] = 0;
        using p_t = pair<Cost, u32>;
        $ que = priority_queue<p_t, vector<p_t>, greater<>>{};
        que.emplace(Cost(), start);
        while (!que.empty()) {
            $ C p = que.top();
            que.pop();
            $ C u = p.second;
            if (dis[start][u] < p.first) {
                continue;
            }
            for ($$ e : g[u]) {
                if (relax(start, u, e)) {
                    que.emplace(dis[start][e.to], e.to);
                }
            }
        }
    }
};

#pragma endregion

```
