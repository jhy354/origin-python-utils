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
    return [math.radians(v) if isinstance(v, (int, float)) else 0.0 for v in deg]


def rad2deg(rad: list) -> list:
    return [math.degrees(v) if isinstance(v, (int, float)) else 0.0 for v in rad]
