# k维树

```cpp
#pragma region k-dimensional tree

// 辅助函数，相当于先push再pop
template <typename E>
$ push_pop(vector<E>& v, E const& e) {
    if (e < v.front()) {
        pop_heap(v.begin(), v.end());
        v.back() = e;
        push_heap(v.begin(), v.end());
    }
}

// k维树，维数为K，坐标type为Crd（不可为unsigned），其他信息type为Other
template <u32 K, typename Crd, typename Other>
class kdt {
public:
    using crd_arr_t = array<Crd, K>;

    class point {
    public:
        crd_arr_t crd;
        Other other;

        point(crd_arr_t const& crd_in, Other const& other_in): crd(crd_in), other(move(other_in)) {
        }
    };

private:
    u32 root_ = 0;
    vector<u32> axis_, lc_, rc_;
    vector<point>& points_;

    // 以 [first, last) 中的点建树，返回此树的root
    $ build(u32 const& first, u32 const& last) -> u32 {
        $C r = choose_axis(first, last);
        $C num = last - first;
        $C mid = first + num / 2;
        if (num == 1) {
        }
        else if (num == 2) {
            axis_[mid] = r;
            (points_[first].crd[r] <= points_[mid].crd[r] ? lc_[mid] : rc_[mid]) = first;
        }
        else {
            $C b = points_.begin();
            nth_element(b + first, b + mid, b + last,
                        [&](point const& x, point const& y) {
                            return x.crd[r] < y.crd[r];
                        }
            );
            axis_[mid] = r;
            lc_[mid] = build(first, mid);
            rc_[mid] = build(mid + 1, last);
        }
        return mid;
    }

    // 选择 [first, last) 中方差最大的维度
    $ choose_axis(u32 const& first, u32 const& last) const {
        u32 ret_axis = 0;
        float var_max = 0;
        for (u32 i = 0; i < K; ++i) {
            $ var_i = variance(first, last, i);
            if (var_i > var_max) {
                var_max = var_i;
                ret_axis = i;
            }
        }
        return ret_axis;
    }

    // 计算 [first, last) 中，维度r的方差
    $ variance(u32 const& first, u32 const& last, u32 const& r) const {
        $ sum_x = 0.0f, sum_x2 = 0.0f;
        for ($ i = first; i != last; ++i) {
            $C tmp = static_cast<float>(points_[i].crd[r]);
            sum_x += tmp;
            sum_x2 += tmp * tmp;
        }
        return sum_x2 - sum_x * sum_x / static_cast<float>(last - first);
    }

public:
    // 以vector<point>初始化，之后外部不应修改此vector
    explicit kdt(vector<point>& points_in) : points_(points_in) {
        $C sz = points_.size();
        axis_.resize(sz);
        lc_.resize(sz, inf);
        rc_.resize(sz, inf);
        root_ = build(0, sz);
    }

private:
    class ret_t {
    public:
        double dis;
        Other other;
        $ operator<(ret_t const& a) const {
            return tie(this->dis, this->other) < tie(a.dis, a.other);
        }
    };

    ret_t none_{numeric_limits<double>::infinity(), Other()};

    // 返回px的欧氏距离的平方，使用浮点数避免平方后溢出
    $ dis2(crd_arr_t const& p, u32 const& x) {
        double ret = 0;
        for (u32 i = 0; i != K; ++i) {
            $C dis1 = static_cast<double>(p[i]) - static_cast<double>(points_[x].crd[i]);
            ret += dis1 * dis1;
        }
        return sqrt(ret);
    }

public:
    // 返回距离点p最近的k个点，欧氏距离
    $ knn(crd_arr_t const& p, u32 const& k) {
        vector<ret_t> ret(k, none_);
        function<void(u32)> dfs = [&](u32 const& x) {
            if (x != inf) {
                $C r = axis_[x];
                $C dis_sp = p[r] - points_[x].crd[r];
                $C left = dis_sp <= 0;
                dfs(left ? lc_[x] : rc_[x]);
                $C tmp = ret_t{dis2(p, x), points_[x].other};
                push_pop(ret, tmp);
                if (abs(dis_sp) <= ret.front().dis) {
                    dfs(left ? rc_[x] : lc_[x]);
                }
            }
        };
        dfs(root_);
        sort_heap(ret.begin(), ret.end());
        ret.erase(lower_bound(ret.begin(), ret.end(), none_), ret.end());
        return ret;
    }
};

// k维树，维数为2的特化
template <typename Crd, typename Other>
class kdt<2, Crd, Other> {
public:
    using crd_arr_t = array<Crd, 2>;

    class point {
    public:
        crd_arr_t crd;
        Other other;

        point(crd_arr_t const& crd_in, Other const& other_in): crd(crd_in), other(move(other_in)) {
        }
    };

private:
    u32 root_ = 0;
    vector<u32> lc_, rc_;
    vector<bool> axis_;
    vector<point>& points_;

    // 以 [first, last) 中的点建树，返回此树的root
    $ build(u32 const& first, u32 const& last) -> u32 {
        $C r = choose_axis(first, last);
        $C num = last - first;
        $C mid = first + num / 2;
        if (num == 1) {
        }
        else if (num == 2) {
            axis_[mid] = r;
            (points_[first].crd[r] <= points_[mid].crd[r] ? lc_[mid] : rc_[mid]) = first;
        }
        else {
            $C b = points_.begin();
            nth_element(b + first, b + mid, b + last,
                        [&](point const& x, point const& y) {
                            return x.crd[r] < y.crd[r];
                        }
            );
            axis_[mid] = r;
            lc_[mid] = build(first, mid);
            rc_[mid] = build(mid + 1, last);
        }
        return mid;
    }

    // 选择 [first, last) 中方差最大的维度
    $ choose_axis(u32 const& first, u32 const& last) const {
        return variance(first, last, false) < variance(first, last, true);
    }

    // 计算 [first, last) 中，维度r的方差
    $ variance(u32 const& first, u32 const& last, bool const& r) const {
        $ sum_x = 0.0f, sum_x2 = 0.0f;
        for ($ i = first; i != last; ++i) {
            $C tmp = static_cast<float>(points_[i].crd[r]);
            sum_x += tmp;
            sum_x2 += tmp * tmp;
        }
        return sum_x2 - sum_x * sum_x / static_cast<float>(last - first);
    }

public:
    // 以vector<point>初始化，之后外部不应修改此vector
    explicit kdt(vector<point>& points_in) : points_(points_in) {
        $C sz = points_.size();
        axis_.resize(sz);
        lc_.resize(sz, inf);
        rc_.resize(sz, inf);
        root_ = build(0, sz);
    }

private:
    class ret_t {
    public:
        double dis;
        Other other;
        $ operator<(ret_t const& a) const {
            return tie(this->dis, this->other) < tie(a.dis, a.other);
        }
    };

    ret_t none_{numeric_limits<double>::infinity(), Other()};

    // 返回px的欧氏距离的平方，使用浮点数避免平方后溢出
    $ dis2(crd_arr_t const& p, u32 const& x) {
        $C dis_x = static_cast<double>(p[0]) - static_cast<double>(points_[x].crd[0]);
        $C dis_y = static_cast<double>(p[1]) - static_cast<double>(points_[x].crd[1]);
        return sqrt(dis_x * dis_x + dis_y * dis_y);
    }

public:
    // 返回距离点p最近的k个点，欧氏距离
    $ knn(crd_arr_t const& p, u32 const& k) {
        vector<ret_t> ret(k, none_);
        function<void(u32)> dfs = [&](u32 const& x) {
            if (x != inf) {
                $C r = axis_[x];
                $C dis_sp = p[r] - points_[x].crd[r];
                $C left = dis_sp <= 0;
                dfs(left ? lc_[x] : rc_[x]);
                $C tmp = ret_t{dis2(p, x), points_[x].other};
                push_pop(ret, tmp);
                if (abs(dis_sp) <= ret.front().dis) {
                    dfs(left ? rc_[x] : lc_[x]);
                }
            }
        };
        dfs(root_);
        sort_heap(ret.begin(), ret.end());
        ret.erase(lower_bound(ret.begin(), ret.end(), none_), ret.end());
        return ret;
    }
};

#pragma endregion

```
