# Origin Python Utils

基于 [OriginLab](https://www.originlab.com/) 的 Python 自定义函数库，专用于**设置列值**（Set Column Values）和 LabTalk 脚本调用。

---

## 概述

本库提供按行跨列统计计算、单列变换以及角度单位换算函数。所有实现均遵循 Origin 严格类型要求，避免 **ERR0015110** 报错（详见[故障排查指南](./docs/origin-python-ERR0015110.md)）。

## 函数列表

### 描述性统计

| 函数 | 说明 |
|---|---|
| `avg_col(*args)` | 按行计算多列算术平均值，忽略非数值 |
| `sd_col(*args)` | 按行计算样本标准差（ddof=1） |
| `rsd_col(*args)` | 按行计算相对标准偏差（%），即变异系数 |
| `sem_col(*args)` | 按行计算平均值的标准误（SD / √n） |
| `mad_col(*args)` | 按行计算中位数绝对偏差，稳健离散度指标 |

### 稳健与专用统计

| 函数 | 说明 |
|---|---|
| `iqr_col(*args)` | 按行计算四分位距（Q3 - Q1），至少需 4 个有效值 |
| `trimmean_col(*args, percent=20)` | 按行计算切尾均值，默认去掉首尾各 10% |
| `geomean_col(*args)` | 按行计算几何平均数，含非正数返回 0 |
| `harmean_col(*args)` | 按行计算调和平均数，含非正数返回 0 |

### 标准化

| 函数 | 说明 |
|---|---|
| `zscore_col(vals)` | 单列 Z-score 标准化（减均值除以标准差） |

### 角度换算

| 函数 | 说明 |
|---|---|
| `deg2rad(deg)` | 角度转弧度（逐元素） |
| `rad2deg(rad)` | 弧度转角度（逐元素） |

## 在 Origin 中使用

### 方法一：复制到 labtalk.py（最简）

Origin 默认从**用户文件文件夹**（UFF）下的 `labtalk.py` 加载 Python 函数。

1. 菜单 **Connectivity > Open Default Python Functions...**
2. 将 `src/oristats.py` 中所需函数复制到 `labtalk.py`
3. 在**设置列值**对话框或 LabTalk 脚本中用 `py.` 前缀调用：

```labtalk
col(B) = py.avg_col(col(C), col(D), col(E));
col(F) = py.sd_col(col(C), col(D), col(E));
col(G) = py.rsd_col(col(C), col(D), col(E));
```

### 方法二：直接使用 oristats.py

将 `src/oristats.py` 放入 UFF，通过文件名前缀调用：

```labtalk
col(B) = py.oristats.avg_col(col(C), col(D), col(E));
col(F) = py.oristats.sd_col(col(C), col(D), col(E));
```

### 方法三：自定义路径

通过 Python 对象属性设置自定义目录和文件名：

```labtalk
Python.LTwd$ = "D:\Python";
Python.LTwf$ = "oristats.py";
col(B) = py.avg_col(col(C), col(D), col(E));
```

设定后保存在 `Origin.ini` 中，跨会话持久生效。

> **注意：** `py.` 语法在设置列值对话框和 LabTalk 脚本窗口中均可使用，无需 `import` 语句。

## Origin 兼容性说明

为避免 ERR0015110 错误，所有函数遵循以下规范：

- 返回**纯 Python float 列表**（Origin 的 C 接口拒绝 `int`、`numpy.float64` 等类型）
- 使用 `try: val = float(val)` 而非 `isinstance()`，以兼容 Origin 列中的 `numpy.float64` 等类型
- 避免**生成器表达式**（`sum(x for x in vals)`），改用显式 `for` 循环
- 避免在可能为负的值上使用 `math.sqrt()`，改用 `** 0.5`
- 所有返回值均显式 `float()` 转换

## 故障排查

Origin 报错 **ERR0015110** 时，参见 [`docs/origin-python-ERR0015110.md`](./docs/origin-python-ERR0015110.md) 获取完整排查清单。

## 项目结构

```
origin-python-utils/
├── src/
│   └── oristats.py              # 函数定义
├── docs/
│   └── origin-python-ERR0015110.md  # 故障排查指南
├── README.md                    # 英文版
├── README_zh.md                 # 本文件（中文版）
└── .gitignore
```
