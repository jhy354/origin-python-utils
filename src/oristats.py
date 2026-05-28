"""
记得 git push
"""
import math


def avg_col(*args: list) -> list:
    max_len = max(len(lst) for lst in args)
    avg_result = []

    for i in range(max_len):
        sum_i = 0
        count = 0

        for lst in args:
            if i >= len(lst):
                continue
            val = lst[i]
            try:
                val = float(val)
            except:
                continue
            sum_i += val
            count += 1

        if count > 0:
            avg_result.append(sum_i / count)
        else:
            avg_result.append(0)

    return avg_result


def sd_col(*args):
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

        n = len(vals)
        if n < 2:
            result.append(0.0)
        else:
            s = 0.0
            for v in vals:
                s += v
            m = s / n
            ss = 0.0
            for v in vals:
                ss += (v - m) ** 2
            var = ss / (n - 1)
            if var <= 0:
                result.append(0.0)
            else:
                result.append(float(var ** 0.5))

    return result


def rsd_col(*args):
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

        n = len(vals)
        if n < 2:
            result.append(0.0)
        else:
            s = 0.0
            for v in vals:
                s += v
            m = s / n
            if m == 0:
                result.append(0.0)
            else:
                ss = 0.0
                for v in vals:
                    ss += (v - m) ** 2
                var = ss / (n - 1)
                if var <= 0:
                    result.append(0.0)
                else:
                    result.append(float(var ** 0.5 / m * 100))

    return result


def deg2rad(deg: list) -> list:
    """Convert degrees to radians element-wise. Non-numeric inputs yield 0."""
    return [math.radians(v) if isinstance(v, (int, float)) else 0.0 for v in deg]


def rad2deg(rad: list) -> list:
    """Convert radians to degrees element-wise. Non-numeric inputs yield 0."""
    return [math.degrees(v) if isinstance(v, (int, float)) else 0.0 for v in rad]


def sem_col(*args):
    """Standard error of the mean (SD / sqrt(n)) computed row-wise across multiple columns."""
    max_len = max(len(lst) for lst in args)
    result = []
    for i in range(max_len):
        vals = []
        for lst in args:
            if i >= len(lst):
                continue
            try:
                vals.append(float(lst[i]))
            except:
                continue
        n = len(vals)
        if n < 2:
            result.append(0.0)
        else:
            s = 0.0
            for v in vals:
                s += v
            m = s / n
            ss = 0.0
            for v in vals:
                ss += (v - m) ** 2
            sd = (ss / (n - 1)) ** 0.5
            result.append(float(sd / (n ** 0.5)))
    return result


def zscore_col(vals):
    """Z-score standardization of a single column. Subtracts column mean and divides by standard deviation."""
    fvals = []
    for v in vals:
        try:
            fvals.append(float(v))
        except:
            continue
    n = len(fvals)
    if n < 2:
        return [0.0] * len(vals)
    s = 0.0
    for v in fvals:
        s += v
    m = s / n
    ss = 0.0
    for v in fvals:
        ss += (v - m) ** 2
    sd = (ss / (n - 1)) ** 0.5
    if sd == 0:
        return [0.0] * len(vals)
    result = []
    for v in vals:
        try:
            result.append(float((float(v) - m) / sd))
        except:
            result.append(0.0)
    return result


def mad_col(*args):
    """Median absolute deviation computed row-wise across multiple columns. A robust alternative to standard deviation."""
    max_len = max(len(lst) for lst in args)
    result = []
    for i in range(max_len):
        vals = []
        for lst in args:
            if i >= len(lst):
                continue
            try:
                vals.append(float(lst[i]))
            except:
                continue
        n = len(vals)
        if n == 0:
            result.append(0.0)
        else:
            vals.sort()
            if n % 2 == 1:
                med = float(vals[n // 2])
            else:
                med = float((vals[n // 2 - 1] + vals[n // 2]) / 2.0)
            devs = []
            for v in vals:
                d = v - med
                if d < 0:
                    d = -d
                devs.append(d)
            devs.sort()
            m = len(devs)
            if m % 2 == 1:
                result.append(float(devs[m // 2]))
            else:
                result.append(float((devs[m // 2 - 1] + devs[m // 2]) / 2.0))
    return result


def iqr_col(*args):
    """Interquartile range (Q3 - Q1) computed row-wise across multiple columns. Requires at least 4 valid values per row."""
    max_len = max(len(lst) for lst in args)
    result = []

    def _pct(sv, p):
        idx = p / 100.0 * (len(sv) - 1)
        lo = int(idx)
        hi = lo + 1
        if hi >= len(sv):
            return float(sv[lo])
        frac = idx - lo
        return float(sv[lo] * (1.0 - frac) + sv[hi] * frac)

    for i in range(max_len):
        vals = []
        for lst in args:
            if i >= len(lst):
                continue
            try:
                vals.append(float(lst[i]))
            except:
                continue
        n = len(vals)
        if n < 4:
            result.append(0.0)
        else:
            vals.sort()
            q1 = _pct(vals, 25)
            q3 = _pct(vals, 75)
            result.append(float(q3 - q1))
    return result


def trimmean_col(*args, percent=20):
    """Trimmed (truncated) mean row-wise across columns. Removes the smallest and largest (percent/2)% before averaging."""
    max_len = max(len(lst) for lst in args)
    result = []
    for i in range(max_len):
        vals = []
        for lst in args:
            if i >= len(lst):
                continue
            try:
                vals.append(float(lst[i]))
            except:
                continue
        n = len(vals)
        if n == 0:
            result.append(0.0)
        else:
            vals.sort()
            k = int(n * percent / 100.0 / 2.0)
            if k * 2 >= n:
                result.append(0.0)
            else:
                s = 0.0
                for j in range(k, n - k):
                    s += vals[j]
                result.append(float(s / (n - 2 * k)))
    return result


def geomean_col(*args):
    """Geometric mean computed row-wise across multiple columns. Returns 0 if any value is non-positive."""
    max_len = max(len(lst) for lst in args)
    result = []
    for i in range(max_len):
        vals = []
        for lst in args:
            if i >= len(lst):
                continue
            try:
                vals.append(float(lst[i]))
            except:
                continue
        n = len(vals)
        if n == 0:
            result.append(0.0)
        else:
            p = 1.0
            for v in vals:
                p *= v
            if p <= 0:
                result.append(0.0)
            else:
                result.append(float(p ** (1.0 / n)))
    return result


def harmean_col(*args):
    """Harmonic mean computed row-wise across multiple columns. Returns 0 if any value is non-positive."""
    max_len = max(len(lst) for lst in args)
    result = []
    for i in range(max_len):
        vals = []
        for lst in args:
            if i >= len(lst):
                continue
            try:
                vals.append(float(lst[i]))
            except:
                continue
        n = len(vals)
        if n == 0:
            result.append(0.0)
        else:
            s = 0.0
            ok = True
            for v in vals:
                if v <= 0:
                    ok = False
                    break
                s += 1.0 / v
            if ok and s > 0:
                result.append(float(n / s))
            else:
                result.append(0.0)
    return result
