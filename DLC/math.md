# 数学

数学有很多分支，因为依赖关系错综复杂所以直接合在一起了

有些东西写成类可能比较奇怪，但我暂时想不到更好的封装方法

------

```cpp
#pragma region math

#pragma region qpow and prime and phi

// 快速幂，不取模
template <typename Int1, typename Int2>
$ constexpr qpow(Int1 base, Int2 e) {
    Int1 ret = 1;
    for (; e; e >>= 1, base *= base) {
        if (e & 1) {
            ret *= base;
        }
    }
    return ret;
}

// 快速幂，不依赖Mod素性
template <$ Mod, typename Int1, typename Int2>
$ constexpr qpow_not_prime(Int1 base, Int2 e) {
    static_assert(Mod > 1);
    Int1 ret = 1;
    for (base %= Mod; e; e >>= 1, base = base * base % Mod) {
        if (e & 1) {
            ret = ret * base % Mod;
        }
    }
    return ret;
}

// 快速幂，Mod为素数，基于费马小定理优化
template <$ Mod, typename Int1, typename Int2>
$ constexpr qpow_prime(Int1 base, Int2 e) {
    return qpow_not_prime<Mod>(base, e % (Mod - 1));
}

// 素数直接检测
class prime {
    // 此class仅用作封装，不应实例化
    prime() = delete;

public:
    // 基于费马小定理，进行Miller–Rabin素性测试
    $ static constexpr check(i64 const& n) {
        $ checker = array{2, 3, 5, 7, 11, 13, 17, 19, 23};
        for ($$ i : checker) {
            if (n % i == 0) {
                return n == i;
            }
        }
        if (n < checker.back()) {
            return false;
        }
        i64 s = 0;
        $ t = n - 1;
        while ((t & 1) != 0) {
            t >>= 1;
            ++s;
        }
        for ($$ i : checker) {

            // qpow
            i64 ret = 1;
            $ base = i % n, e = t;
            for (; e != 0; e >>= 1, base = base * base % n) {
                if ((e & 1) != 0) {
                    ret = ret * base % n;
                }
            }
            // qpow over

            if (ret == 1) {
                continue;
            }
            auto ok = false;
            for ($ j = 0; j < s && !ok; ++j) {
                if (ret == n - 1) {
                    ok = true;
                }
                ret = ret * ret % n;
            }
            if (!ok) {
                return false;
            }
        }
        return true;
    }
};

// 素数表
template <size_t N>
class prime_arr {
public:
    array<u32, N> pri{};
    u32 cnt = 0;

    // 欧拉筛法，O(n)，编译期计算
    constexpr prime_arr() {
        array<bool, N> vis{};
        for (u32 i = 2; i < N; ++i) {
            if (!vis[i]) {
                pri[cnt++] = i;
            }
            for (u32 j = 0; j < cnt; ++j) {
                if (static_cast<u64>(i) * pri[j] >= N) {
                    break;
                }
                vis[i * pri[j]] = true;
                if (!(i % pri[j])) {
                    break;
                }
            }
        }
    }
};

// 欧拉函数表
template <size_t N>
class phi_arr {
public:
    array<u32, N> phi{};

    constexpr phi_arr() {
        phi[1] = 1;
        for (u32 i = 2; i < N; ++i) {
            if (!phi[i]) {
                for ($ j = i; j < N; j += i) {
                    if (!phi[j]) {
                        phi[j] = j;
                    }
                    phi[j] = phi[j] / i * (i - 1);
                }
            }
        }
    }
};

// 素数表 + 欧拉函数表
template <size_t N>
class prime_phi_arr {
public:
    array<u32, N> pri{};
    array<u32, N> phi{};
    u32 cnt = 0;

    // 欧拉筛法，O(n)，编译期计算
    constexpr prime_phi_arr() {
        array<bool, N> vis{};
        phi[1] = 1;
        for (u32 i = 2; i < N; ++i) {
            if (!vis[i]) {
                pri[cnt++] = i;
                phi[i] = i - 1;
            }
            for (u32 j = 0; j < cnt; ++j) {
                if (static_cast<u64>(i) * pri[j] >= N) {
                    break;
                }
                $ idx = i * pri[j];
                vis[idx] = true;
                if (i % pri[j]) {
                    phi[idx] = phi[i] * (pri[j] - 1);
                }
                else {
                    phi[idx] = phi[i] * pri[j];
                    break;
                }
            }
        }
    }
};

// 快速幂，自动判断Mod是否为素数
template <$ Mod, typename Int1, typename Int2>
$ constexpr qpow(Int1 base, Int2 e) {
    if constexpr (prime::check(Mod)) {
        return qpow_prime<Mod>(base, e);
    }
    else {
        return qpow_not_prime<Mod>(base, e);
    }
}

#pragma endregion

#pragma region inv and fac and comb

// 逆元
template <$ Mod>
class inv {
    // 此class仅用作封装，不应实例化
    inv() = delete;

public:
    // 非素数遇到再写吧
    static_assert(prime::check(Mod));

    // 基于费马小定理
    $ static constexpr inv_prime(i64 const& x) {
        return qpow<Mod>(x, Mod - 2);
    }
};

// 阶乘及其逆元，Start不为0时推广为前缀积
template <$ Mod, size_t N, i64 Start = 0>
class fac_arr {
    // 否则fac为0逆元无意义
    static_assert(Start + N <= Mod);
public:
    array<i64, N> fac{};
    array<i64, N> fac_inv{};

    constexpr fac_arr() {
        fac[0] = Start != 0 ? Start : 1;
        for (u32 i = 1; i < N; ++i) {
            fac[i] = fac[i - 1] * (Start + i) % Mod;
        }
        fac_inv[N - 1] = inv<Mod>::inv_prime(fac[N - 1]);
        for ($ i = N - 1; i > 0; --i) {
            fac_inv[i - 1] = fac_inv[i] * (Start + i) % Mod;
        }
    }
};

// 逆元表，[Start, Start + N)
template <$ Mod, size_t N, i64 Start = 0>
class inv_arr {
public:
    array<i64, N> arr{};

    // 懒癌写法，能用就行
    constexpr inv_arr() {
        constexpr fac_arr<Mod, N, Start> tmp;
        for (u32 i = 1; i < N; ++i) {
            arr[i] = tmp.fac[i - 1] * tmp.fac_inv[i] % Mod;
        }
    }
};

// 组合数，需要用fac_arr来初始化
template <$ Mod, size_t N>
class comb {
    const fac_arr<Mod, N>& fac_;

    // 直接利用组合数公式，需要 n < N
    $ comb1(u32 const& n, u32 const& m) const {
        return n < m ? 0 : fac_.fac[n] * fac_.fac_inv[m] % Mod * fac_.fac_inv[n - m] % Mod;
    }

    // 基于Lucas定理，需要 Mod == N
    $ comb2(i64 const& n, i64 const& m) const -> i64 {
        return m != 0 ? comb1(static_cast<u32>(n % Mod), static_cast<u32>(m % Mod)) * comb2(n / Mod, m / Mod) % Mod : 1;
    }

public:
    explicit comb(fac_arr<Mod, N> const& fac_in) : fac_(fac_in) {
    }

    // 求n取m的组合数，自动选择合适的算法
    $ operator()(i64 const& n, i64 const& m) const {
        if (n < N) {
            return comb1(static_cast<u32>(n), static_cast<u32>(m));
        }
        if constexpr (Mod == N) {
            return comb2(n, m);
        }
        else {
            throw invalid_argument("表太小不够用");
        }
    }
};

#pragma endregion

#pragma endregion

$ main() -> int {
    ccxxxi();

    cout << qpow(2, 10) << "\n";
    cout << qpow<100>(2, 10) << "\n";
    cout << qpow<1021>(2, 10) << "\n";

    $ constexpr test = prime::check(998'244'353);
    cout << boolalpha << test << "\n";

    $ constexpr pri = prime_arr<200>{};
    cout << pri.cnt << " " << pri.pri[pri.cnt - 1] << "\n";

    $C c = comb(fac_arr<7, 7>{});
    cout << c(5, 2) << "\n";
}

```