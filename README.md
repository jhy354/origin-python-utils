# Origin Python Utils

Custom Python functions for [OriginLab](https://www.originlab.com/) — designed for use in **Set Column Values** and other Origin Python scripting contexts.

Origin 自定义 Python 函数库，专用于 **设置列值（Set Column Values）** 及其他 Origin Python 脚本场景。

## Functions

| Function | Description | 说明 |
|---|---|---|
| `avg_col(*args)` | Row-wise arithmetic mean across multiple columns | 按行计算多列算术平均值 |
| `sd_col(*args)` | Row-wise sample standard deviation (ddof=1) | 按行计算样本标准差（ddof=1） |
| `rsd_col(*args)` | Row-wise relative standard deviation (%) | 按行计算相对标准偏差（%） |
| `sem_col(*args)` | Row-wise standard error of the mean (SD/√n) | 按行计算平均值的标准误 |
| `zscore_col(vals)` | Z-score standardization of a single column | 单列 Z-score 标准化 |
| `mad_col(*args)` | Row-wise median absolute deviation (robust dispersion) | 按行计算中位数绝对偏差（稳健离散度） |
| `iqr_col(*args)` | Row-wise interquartile range (Q3-Q1), needs ≥4 values | 按行计算四分位距，至少需 4 个值 |
| `trimmean_col(*args)` | Row-wise trimmed mean (default: remove 20% extremes) | 按行计算切尾均值（默认去掉首尾各 10%） |
| `geomean_col(*args)` | Row-wise geometric mean | 按行计算几何平均数 |
| `harmean_col(*args)` | Row-wise harmonic mean | 按行计算调和平均数 |
| `deg2rad(deg)` | Convert degrees to radians (vectorized) | 角度转弧度（向量化） |
| `rad2deg(rad)` | Convert radians to degrees (vectorized) | 弧度转角度（向量化） |

## Usage in Origin

1. Place `myfunc.py` in a directory accessible to Origin's Python environment.
2. In **Set Column Values** dialog, import and call:

```python
import myfunc
col(A) = myfunc.avg_col(col(B), col(C), col(D))
col(E) = myfunc.sd_col(col(B), col(C), col(D))
col(F) = myfunc.rsd_col(col(B), col(C), col(D))
```

### Important Notes for Origin Compatibility

All functions are written with Origin's strict type requirements in mind:

- Returns **pure Python `float`** lists (Origin's C interface rejects `int`, `numpy.float64`, etc.)
- Uses **`try: val = float(val)`** instead of `isinstance()` to accept Origin column types like `numpy.float64`
- Avoids **generator expressions** (`sum(x for x in vals)`) — uses explicit `for` loops instead
- Avoids **`math.sqrt()`** on potentially negative float values — uses `** 0.5` instead
- All return values are explicitly cast with `float()`

## Troubleshooting

If Origin reports error **ERR0015110** ("调用的 Python 函数没有返回可以转换为双精度值的值"), see [`origin-python-ERR0015110.md`](./origin-python-ERR0015110.md) for a detailed diagnosis and fix checklist.

## Files

- `myfunc.py` — Function definitions
- `origin-python-ERR0015110.md` — ERR0015110 error troubleshooting guide (Chinese)
