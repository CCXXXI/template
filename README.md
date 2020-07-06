# template

 一些常用的或不常用的代码模板

日常刷题整理，作为备份兼分享同步至GitHub

## 个人偏好

我常常觉得自己一个月前写出的代码很丑，所以风格和环境偏好也一直在变，这里记录一些变化相对不大的内容

### python

* 代码风格完全按照[yapf](https://github.com/google/yapf)默认配置
  * yapf非常严格以至于写代码时几乎不需要考虑格式，perfect
* IDE偏好[PyCharm](https://www.jetbrains.com/pycharm/)，代码风格整理稍微弱了点，用yapf补足之后基本完美
* python + numpy已经足够强大，所以基本没有模板

### cpp

* 代码风格大部分按照[ReSharper](https://www.jetbrains.com/dotnet/)默认配置，以下例外：
  * 缩进设定为4个空格
    * 为了在各个平台上阅读时，至少缩进宽度保持不变
  * 括号设定为[K&R style](https://en.wikipedia.org/wiki/Indentation_style#K&R_style)
    * 因为习惯于通过缩进而不是大括号来识别逻辑层次
    * [Lisp style](https://en.wikipedia.org/wiki/Indentation_style#Lisp_style)（或者叫Python style）更符合要求，但主流IDE一般不支持这个，只好退而求其次
  * Cleanup Code启用所有选项
    * 理由同yapf
  * 完全禁用Clang-Tidy检查
    * Clang-Tidy太严格了，而且给出的warning有太多是想修复也无从下手的
* IDE偏好[Visual Studio](https://visualstudio.microsoft.com/)
  * 备选[CLion](https://www.jetbrains.com/clion/)
* 本地环境偏好开到c++latest，但是为了方便在OJ上用，尽量兼容c++17
  * 代码会在msvc和gcc下分别测试
  * 两者都支持的特性，即使未被标准规定，也可能会使用
    * 比如把`$`用于标识符
  * 两者至少之一不支持的特性不会使用
    * 例外：`#include<bits/stdc++.h>`，这个文件会从gcc复制一份到代码目录

## 参考资料

部分资料有多种语言版本，中文版更新常常滞后于英文版（悲）

* 模板
  * [F0RE1GNERS](https://github.com/F0RE1GNERS)/[template](https://github.com/F0RE1GNERS/template)
  * [LzyRapx](https://github.com/LzyRapx)/[Algorithmic_Template](https://github.com/LzyRapx/Algorithmic_Template)
* 文档
  * [Python中文文档](https://docs.python.org/zh-cn/3/index.html)
  * [cppreference](https://zh.cppreference.com/)
  * [NumPy 中文](https://www.numpy.org.cn/)
* 工具
  * [Compiler Explorer](https://godbolt.org/)
  * [Data Structure Visualizations](https://www.cs.usfca.edu/~galles/visualization/Algorithms.html)
* 检索
  * [stackoverflow](https://stackoverflow.com/)
  * [OI Wiki](https://oi-wiki.org/)
  * [OEIS](https://oeis.org/)
  * [GitHub](https://github.com/)
  * [Google](https://www.google.com/)
