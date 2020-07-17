# 图

```cpp
#pragma region graph

// 带边权的图，存储为邻接表
class graph_with_cost {
    class edge {
    public:
        u32 to;
        i32 cost;
    };

public:
    vector<vector<edge>> g;
    u32 sz;

    explicit graph_with_cost(u32 C& sz_in) : sz(sz_in) {
        g.resize(sz);
    }

    // 添加u到v，权值为cost的单向边
    $ add(u32 C& u, u32 C& v, i32 C& cost) {
        g[u].push_back(edge{ v, cost });
    }

    // 添加uv之间，权值为cost的双向边
    $ add2(u32 C& u, u32 C& v, i32 C& cost) {
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
                if ((color[u] == 0) and !dfs(u, -c)) {
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

    // Bellman-Ford算法，队列优化，仅用于有负权时的单源最短路
    $ bf(u32 C& start)C {
        $ que = queue<u32>{};
        que.push(start);
        $ in_que = vector<bool>(sz);
        while(!que.empty()) {
            $ C u=que.front();que.pop();
            in_que[u]=false;
        }
    }

};

#pragma endregion

```
