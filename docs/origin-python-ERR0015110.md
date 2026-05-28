# Origin ERR0015110 错误原因

## 错误信息

> ERR0015110: 调用的 Python 函数 %s 没有返回可以转换为双精度值的值

## 原因

OriginLab 的 Python 接口在解析 Python 函数时，如果函数定义中包含 **docstring**（多行字符串文档注释），会导致 Origin 无法正确识别函数的返回值类型，从而报错 ERR0015110。

## 解决方案

删除 Python 脚本中所有函数的 docstring。即使 docstring 只是被 Python 解释器忽略的普通字符串，Origin 的 Python 接口在解析时仍会因此无法正确处理函数的返回值。

## 影响范围

`oristats.py` 中的所有函数均受到影响，包括但不限于：`avg_col`、`sd_col`、`rsd_col`、`deg2rad`、`rad2deg`、`sem_col`、`zscore_col`、`mad_col`、`iqr_col`、`trimmean_col`、`geomean_col`、`harmean_col`。

## 验证

删除 docstring 后，所有函数在 Origin 中均可正常调用并返回双精度值。
