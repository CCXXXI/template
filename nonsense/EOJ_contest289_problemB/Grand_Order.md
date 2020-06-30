# 期末大作业特化版二维kd树

通用版在[这里](/DLC/geometry/k-d_tree.md)，下面是仅对此次作业表现比较好的版本

以【特化：】开头的注释表示面向测试数据的优化

------

```cpp
#pragma region 2-dimensional tree

// 辅助函数，相当于先push再pop
template <typename E>
$ push_pop(vector<E>& v, E const& e) {
    if (e < v.front()) {
        pop_heap(v.begin(), v.end());
        v.back() = e;
        push_heap(v.begin(), v.end());
    }
}

// 期末作业特化版kdt，在build与search的耗时之间取得了绝妙的平衡
template <typename Crd, typename Other>
class _2dt {
public:
    using crd_arr_t = array<Crd, 2>;

    class point {
    public:
        crd_arr_t crd;
        Other other;

        point(crd_arr_t const& crd_in, Other other_in): crd(crd_in), other(std::move(other_in)) {
        }
    };

private:
    u32 root_ = 0;
    vector<u32> lc_, rc_;
    // 特化：不再为每个点存储单独的划分维度，节省了一点点空间
    // vector<bool> axis_;
    bool beg_=false;
    vector<point>& points_;

    // 以 [first, last) 中的点建树，返回此树的root
    // 特化：维度交替选择xy，节省计算方差的时间
    $ build(u32 const& first, u32 const& last,bool const& r) -> u32 {
        // $C r = choose_axis(first, last);
        $C num = last - first;
        $C mid = first + num / 2;
        if (num == 1) {
        }
        else if (num == 2) {
            // axis_[mid] = r;
            (points_[first].crd[r] <= points_[mid].crd[r] ? lc_[mid] : rc_[mid]) = first;
        }
        else {
            $C b = points_.begin();
            nth_element(b + first, b + mid, b + last,
                        [&](point const& x, point const& y) {
                            return x.crd[r] < y.crd[r];
                        }
            );
            // axis_[mid] = r;
            lc_[mid] = build(first, mid,r^1);
            rc_[mid] = build(mid + 1, last,r^1);
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
    explicit _2dt(vector<point>& points_in) : points_(points_in) {
        $C sz = points_.size();
        // 特化：首次分割时，仍然计算方差并选择较优的维度
        beg_=choose_axis(0,sz);
        // axis_.resize(sz);
        lc_.resize(sz, inf);
        rc_.resize(sz, inf);
        root_ = build(0, sz,beg_);
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
        // 特化：经过反复测试，这种看上去很不正常的四舍五入方式是最快的
        return static_cast<double>(static_cast<i32>(sqrt(dis_x * dis_x + dis_y * dis_y) * 1000 + 0.5)) / 1000;
    }

public:
    // 返回距离点p最近的k个点，欧氏距离
    $ knn(crd_arr_t const& p, u32 const& k) {
        vector<ret_t> ret(k, none_);
        function<void(u32,bool)> dfs = [&](u32 const& x,bool const& r) {
            if (x != inf) {
                // $C r = axis_[x];
                $C dis_sp = p[r] - points_[x].crd[r];
                $C left = dis_sp <= 0;
                dfs(left ? lc_[x] : rc_[x],r^1);
                $C tmp = ret_t{dis2(p, x), points_[x].other};
                push_pop(ret, tmp);
                if (abs(dis_sp) <= ret.front().dis) {
                    dfs(left ? rc_[x] : lc_[x],r^1);
                }
            }
        };
        dfs(root_,beg_);
        sort_heap(ret.begin(), ret.end());
        ret.erase(lower_bound(ret.begin(), ret.end(), none_), ret.end());
        return ret;
    }
};

#pragma endregion

```

------

其实还剩一些优化方向没有尝试，如果以上没能把时间压缩到1s以内，以下是可选内容：

* 将所有浮点数换成定点数，节约算力
  * 若此，`sqrt`应替换为牛顿法求平方根
  * 定点数优化：性能成倍提升 - 韦易笑的文章 - 知乎 https://zhuanlan.zhihu.com/p/149517485
* 寻找完美哈希函数
  * 我进行了一些搜索但没能找到简单的解决方案
  * GNU的完美哈希函数生成工具：https://www.gnu.org/software/gperf/manual/gperf.html
  * 文档过于反人类，至今未能学会使用
* 这份资料提到了一些其它算法：https://people.csail.mit.edu/indyk/helsinki-1.pdf
  * 权威性未知
* 这里显示了更多相关的数据结构与算法：https://en.wikipedia.org/wiki/Nearest_neighbor_search
  * 太多了以至于丝毫没有意愿去逐个研究
