# Origin 自定义 Python 函数返回值类型兼容性说明

## 错误信息

在 Origin "设置列值"（Set Column Values）对话框中调用自定义 Python 函数时，系统返回如下错误：

```
ERR0015110: 调用的 Python 函数 %s 没有返回可以转换为双精度值的值。
由于在设置列值脚本中的错误而未能为 std_J 创建操作
```

该错误常见于 `sd_col`、`rsd_col` 等函数，而结构相似的 `avg_col` 函数可正常运行。

---

## 错误成因

### 1. 返回值类型约束

Origin 的 Set Column Values 子系统在底层将 Python 函数返回的列表对象转换为 C 语言 `double[]` 数组。该转换要求列表中的每个元素均为 Python 原生 `float` 类型。以下类型均无法通过转换：

- `numpy.float64`、`numpy.int64` 等 NumPy 数值类型
- Python `int`（即使可隐式转换为 float，Origin 的 C 接口仍拒绝识别）
- `complex`、`Decimal` 等非双精度数值类型
- `None`、`NaN`、`Infinity`
- Origin 自定义数据类型（如 `PyOrigin` 列对象）

### 2. 浮点数精度导致的 math.sqrt 异常

方差的理论值恒为非负数，但浮点数运算的舍入误差可能导致计算结果为极小负数（如 `-1e-16`）。`math.sqrt()` 函数的定义域要求输入非负，输入负数时将抛出 `ValueError`，导致函数整体终止。Origin 收到空返回值后即报告上述错误。

### 3. 生成器表达式的兼容性问题

部分 Origin 内嵌的 Python 发行版对生成器表达式的支持存在局限。以下构造可能引起异常：

```python
sum((x - m) ** 2 for x in vals)   # 潜在兼容性问题
```

改用显式循环可规避该问题：

```python
ss = 0.0
for v in vals:
    ss += (v - m) ** 2
```

### 4. 函数类型注解的潜在干扰

带类型注解的函数签名在部分 Origin 版本中可能导致函数导入异常：

```python
def rsd_col(*args: list) -> list:  # 存在兼容性风险
    ...

def rsd_col(*args):                 # 推荐写法
    ...
```

### 5. 返回列表元素类型不一致

同一返回列表中同时包含 `int`（如 `0`）和 `float`（如计算结果）时，Origin 的类型转换流程可能失败。列表中的所有数值应统一以 `float` 类型表示。

---

## 解决方案

### 输入处理：使用异常捕获替代类型判断

Origin 列元素的运行时类型可能为 `numpy.float64` 等非 Python 原生类型，使用 `isinstance(val, (int, float))` 进行类型筛选会错误排除有效数据。

```python
# 不推荐：会排除 numpy.float64 等有效类型
if not isinstance(val, (int, float)):
    continue

# 推荐：尝试类型转换，失败时跳过
try:
    val = float(val)
except:
    continue
```

### 输出处理：显式指定返回值为 Python float

返回列表中的所有元素应经过显式 `float()` 转换：

```python
# 不推荐：混入 int 类型
result.append(0)
result.append(sd / mean * 100)

# 推荐：全部明确为 float 类型
result.append(0.0)
result.append(float(var ** 0.5 / m * 100))
```

### 写法对照

| 不推荐写法 | 推荐写法 |
|---|---|
| `math.sqrt(variance)` | `var ** 0.5`，或 `math.sqrt(max(v, 0))` |
| `sum((x - m) ** 2 for x in vals)` | 显式 `for` 循环累加 |
| `result.append(0)` | `result.append(0.0)` |
| `def f(*args: list) -> list:` | `def f(*args):` |
| `isinstance(val, (int, float))` | `try: val = float(val)` |

---

## 推荐实现框架

```python
def function_name(*args):
    max_len = max(len(lst) for lst in args)
    result = []

    for i in range(max_len):
        vals = []
        for lst in args:
            if i >= len(lst):
                continue
            val = lst[i]
            try:
                val = float(val)
            except:
                continue
            vals.append(val)

        # 业务计算逻辑
        n = len(vals)
        if n < 2:
            result.append(0.0)
        else:
            # 使用显式循环替代生成器表达式
            s = 0.0
            for v in vals:
                s += v
            m = s / n
            # 计算结果以 float() 显式转换后返回
            result.append(float(computed_value))

    return result
```

---

## 故障排查清单

当 Origin 报告 ERR0015110 错误时，依次检查以下项目：

1. 返回列表中的所有元素是否均为 Python `float` 类型（逐一检查所有 `append` 语句）
2. 是否存在 `math.sqrt()` 调用可能接收负数输入
3. 是否存在生成器表达式
4. 函数定义是否包含类型注解
5. 输入列数据中是否包含缺失值或 Origin 特殊标记（如 `--`）
6. 修改 .py 文件后是否重新执行了 Origin Python 脚本或重新启动了 Origin
7. 返回列表长度是否与目标列行数一致
