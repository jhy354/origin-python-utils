# Origin Python Utils

A collection of Python functions for [OriginLab](https://www.originlab.com/), designed for use in **Set Column Values** and LabTalk scripting.

> [中文版本](./README_zh.md)

## Overview

These functions perform row-wise statistical computations across multiple worksheet columns, single-column transformations, and angle unit conversions. They are implemented with Origin's strict type system in mind to avoid the common **ERR0015110** error (see [troubleshooting guide](./docs/origin-python-ERR0015110.md)).

## Functions

### Descriptive Statistics

| Function | Description |
|---|---|
| `avg_col(*args)` | Row-wise arithmetic mean across columns. Ignores non-numeric values. |
| `sd_col(*args)` | Row-wise sample standard deviation (ddof=1). |
| `rsd_col(*args)` | Row-wise relative standard deviation (%), also known as CV%. |
| `sem_col(*args)` | Row-wise standard error of the mean (SD / sqrt(n)). |
| `mad_col(*args)` | Row-wise median absolute deviation, a robust alternative to SD. |
| `range_col` | — | (Use `max_col` - `min_col` in Origin directly) |

### Robust & Specialized Statistics

| Function | Description |
|---|---|
| `iqr_col(*args)` | Row-wise interquartile range (Q3 - Q1). Requires at least 4 valid values. |
| `trimmean_col(*args, percent=20)` | Row-wise trimmed mean. Removes the smallest and largest `percent/2` % before averaging. |
| `geomean_col(*args)` | Row-wise geometric mean. Returns 0 if any value is non-positive. |
| `harmean_col(*args)` | Row-wise harmonic mean. Returns 0 if any value is non-positive. |

### Standardization

| Function | Description |
|---|---|
| `zscore_col(vals)` | Z-score standardization of a single column (subtracts mean, divides by SD). |

### Angle Conversion

| Function | Description |
|---|---|
| `deg2rad(deg)` | Convert degrees to radians element-wise. |
| `rad2deg(rad)` | Convert radians to degrees element-wise. |

## Usage in Origin

### Method 1: Copy into labtalk.py (Simplest)

Origin loads Python functions from `labtalk.py` in your **User Files Folder (UFF)** by default.

1. Open **Connectivity > Open Default Python Functions...** from the Origin menu.
2. Copy the desired functions from `src/oristats.py` into `labtalk.py`.
3. Call from **Set Column Values** or LabTalk script:

```labtalk
col(B) = py.avg_col(col(C), col(D), col(E));
col(F) = py.sd_col(col(C), col(D), col(E));
col(G) = py.rsd_col(col(C), col(D), col(E));
```

### Method 2: Use the file directly

Place `src/oristats.py` in your **User Files Folder (UFF)** and reference it by filename:

```labtalk
col(B) = py.oristats.avg_col(col(C), col(D), col(E));
col(F) = py.oristats.sd_col(col(C), col(D), col(E));
```

### Method 3: Custom path

Set a custom directory and/or filename via Python object properties:

```labtalk
Python.LTwd$ = "D:\Python";
Python.LTwf$ = "oristats.py";
col(B) = py.avg_col(col(C), col(D), col(E));
```

These properties persist across sessions in `Origin.ini`.

> **Note:** The `py.` syntax works in both the Set Column Values dialog and LabTalk script window. No `import` statement is needed.

## Origin Compatibility Notes

All functions follow these practices to avoid the ERR0015110 error:

- Return **pure Python `float`** lists (Origin's C interface rejects `int`, `numpy.float64`, etc.)
- Use **`try: val = float(val)`** instead of `isinstance()` to accept `numpy.float64` and other non-native types
- Avoid **generator expressions** (`sum(x for x in vals)`), using explicit `for` loops instead
- Avoid **`math.sqrt()`** on potentially negative values, using `** 0.5` instead
- Cast all return values explicitly with `float()`

## Troubleshooting

If Origin reports **ERR0015110**: see [`docs/origin-python-ERR0015110.md`](./docs/origin-python-ERR0015110.md) for a full diagnosis checklist.

## Project Structure

```
origin-python-utils/
├── src/
│   └── oristats.py              # Function definitions
├── docs/
│   └── origin-python-ERR0015110.md  # Troubleshooting guide
├── README.md                    # This file (English)
├── README_zh.md                 # Chinese version
└── .gitignore
```
