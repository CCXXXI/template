# 数学

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

// 快速乘，避免64位整数溢出
template <$ Mod, typename Int1, typename Int2>
$ constexpr mul(Int1 a, Int2 b) {
    $ t = static_cast<i64>(
        static_cast<u64>(a) * b
        - static_cast<u64>(static_cast<long double>(a) * b / Mod) * Mod);
    return static_cast<Int1>(t < 0 ? t + Mod : t);
}

// 快速幂，不依赖Mod素性
template <$ Mod, typename Int1, typename Int2>
$ constexpr qpow_not_prime(Int1 base, Int2 e) {
    static_assert(Mod > 1);
    Int1 ret = 1;
    for (base %= Mod; e; e >>= 1, base = mul<Mod>(base, base)) {
        if (e & 1) {
            ret = mul<Mod>(ret, base);
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
    $ static constexpr check(i64 C& n) {
        $ checker = array{2, 3, 5, 7, 11, 13, 17, 19, 23};

        for ($$ a : checker) {
            if (n % a == 0) {
                return n == a;
            }
        }
        if (n < checker.back()) {
            return false;
        }

        // n == 2^r * d + 1
        i64 r = 0;
        $ d = n - 1;
        while ((d & 1) == 0) {
            d >>= 1;
            ++r;
        }

        // 为了constexpr，mul不能直接调用，让我再次感受到了static_cast的语法设计有多糟糕
        for ($$ a : checker) {
            // x = a^d % n
            i64 x = 1;
            $ base = a % n, e = d;
            for (; e != 0; e >>= 1) {
                if ((e & 1) != 0) {
                    x = static_cast<i64>(
                        static_cast<u64>(x) * base
                        - static_cast<u64>(static_cast<long double>(x) * base / n) * n);
                    if (x < 0) {
                        x += n;
                    }
                }
                base = static_cast<i64>(
                    static_cast<u64>(base) * base
                    - static_cast<u64>(static_cast<long double>(base) * base / n) * n);
                if (base < 0) {
                    base += n;
                }
            }

            if (x == 1) {
                continue;
            }
            $ ok = false;
            for ($ i = 0; i < r && !ok; ++i) {
                if (x == n - 1) {
                    ok = true;
                }
                x = static_cast<i64>(
                    static_cast<u64>(x) * x
                    - static_cast<u64>(static_cast<long double>(x) * x / n) * n);
                if (x < 0) {
                    x += n;
                }
            }
            if (!ok) {
                return false;
            }
        }
        return true;
    }
};

// 素数表
template <u32 N>
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
template <u32 N>
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
template <u32 N>
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

// 求ax+by=gcd(a,b)的解，返回(x,y,d)
$ constexpr ex_gcd(i64 C& a, i64 C& b) {
    if (b == 0) {
        return array<i64, 3>{1, 0, a};
    }
    $$[x, y, d] = ex_gcd(b, a % b);
    return array{y, x - a / b * y, d};
}

// 逆元
template <$ Mod>
class inv_helper {
    // 此class仅用作封装，不应实例化
    inv_helper() = delete;

public:
    // 基于费马小定理
    $ static constexpr inv_prime(i64 C& x) {
        return qpow<Mod>(x, Mod - 2);
    }

    // 基于扩展欧几里得算法
    $ static constexpr inv_not_prime(i64 C& x) {
        $ ret = ex_gcd(x, Mod)[0];
        if (ret < 0) {
            ret += Mod;
        }
        return ret;
    }

};

// 求x的逆元，自动选择合适的算法
template <$ Mod>
$ constexpr inv(i64 C& x) {
    if constexpr (prime::check(Mod)) {
        return inv_helper<Mod>::inv_prime(x);
    }
    return inv_helper<Mod>::inv_not_prime(x);
}

// 阶乘及其逆元，Start不为0时推广为前缀积
template <$ Mod, u32 N, i64 Start = 0>
class fac_arr {
    // 否则fac为0逆元无意义
    static_assert(Start + N <= Mod or Start > Mod);
public:
    array<i64, N> fac{};
    array<i64, N> fac_inv{};

    constexpr fac_arr() {
        $C start = Start % Mod;
        fac[0] = start != 0 ? start : 1;
        for (u32 i = 1; i < N; ++i) {
            fac[i] = fac[i - 1] * ((start + i) % Mod) % Mod;
        }
        fac_inv[N - 1] = inv<Mod>(fac[N - 1]);
        for ($ i = N - 1; i > 0; --i) {
            fac_inv[i - 1] = fac_inv[i] * ((start + i) % Mod) % Mod;
        }
    }
};

// 阶乘及其逆元，Start不为0时推广为前缀积，非constexpr版本
template <$ Mod>
class fac_arr_not_constexpr {
public:
    vector<i64> fac, fac_inv;

    explicit fac_arr_not_constexpr(u32 C& n, i64 start) {
        assert(start + n <= Mod or start > Mod);
        fac.resize(n);
        fac_inv.resize(n);
        fac[0] = start != 0 ? (start %= Mod) : 1;
        for (u32 i = 1; i < n; ++i) {
            fac[i] = fac[i - 1] * ((start + i) % Mod) % Mod;
        }
        fac_inv[n - 1] = inv<Mod>(fac[n - 1]);
        for ($ i = n - 1; i > 0; --i) {
            fac_inv[i - 1] = fac_inv[i] * ((start + i) % Mod) % Mod;
        }
    }
};

// 逆元表，[Start, Start + N)
template <$ Mod, u32 N, i64 Start = 0>
class inv_arr {
public:
    array<i64, N> arr{};

    // 懒癌写法，能用就行
    constexpr inv_arr() {
        constexpr fac_arr<Mod, N, Start> tmp;
        for (u32 i = 1; i < N; ++i) {
            arr[i] = tmp.fac[i - 1] * tmp.fac_inv[i] % Mod;
        }
        if constexpr (Start != 0) {
            arr[0] = inv<Mod>(Start);
        }
    }
};

// 逆元表，[Start, Start + N)，非constexpr版本
template <$ Mod>
class inv_arr_not_constexpr {
public:
    vector<i64> arr;

    // 懒癌写法，能用就行
    explicit inv_arr_not_constexpr(u32 n, i64 start) {
        arr.resize(n);
        fac_arr_not_constexpr<Mod> tmp(n, start);
        for (u32 i = 1; i < n; ++i) {
            arr[i] = tmp.fac[i - 1] * tmp.fac_inv[i] % Mod;
        }
        if (start != 0) {
            arr[0] = inv<Mod>(start);
        }
    }
};

// 组合数，应满足 n < N or Mod == N
template <$ Mod, u32 N>
class comb {
    C fac_arr<Mod, N> fac_{};

    // 直接利用组合数公式，需要 n < N
    $ comb1(u32 C& n, u32 C& m) C {
        return n < m ? 0 : fac_.fac[n] * fac_.fac_inv[m] % Mod * fac_.fac_inv[n - m] % Mod;
    }

    // 基于Lucas定理，需要 Mod == N
    $ comb2(i64 C& n, i64 C& m) C -> i64 {
        return m != 0 ? comb1(static_cast<u32>(n % Mod), static_cast<u32>(m % Mod)) * comb2(n / Mod, m / Mod) % Mod : 1;
    }

public:
    // 求n取m的组合数，自动选择合适的算法
    $ operator()(i64 C& n, i64 C& m) C {
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

    static_assert(qpow(2, 10) == 1024);
    static_assert(qpow<100>(2, 10) == 24);
    static_assert(qpow<1021>(2, 10) == 3);

    static_assert(prime::check(998'244'353));

    $ constexpr pri = prime_arr<200>{};
    static_assert(pri.cnt == 46);
    static_assert(pri.pri[pri.cnt - 1] == 199);

    static_assert(inv<10>(3) == 7);
    static_assert(inv<11>(3) == 4);

    $C c = comb<7, 7>();
    assert(c(5, 2) == 3);
}

```
