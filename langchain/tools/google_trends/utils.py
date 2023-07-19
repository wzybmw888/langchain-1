from __future__ import annotations

from typing import TYPE_CHECKING, Type

import numpy as np
from scipy.stats import norm

if TYPE_CHECKING:
    from pytrends.request import TrendReq


def import_google_trend() -> Type[TrendReq]:
    try:
        from pytrends.request import TrendReq
    except ImportError:
        raise ImportError(
            "You need to install pytrends to use this toolkit. "
            "Try running pip install --upgrade pytrends"
        )
    return TrendReq


def mk_test(x: list, alpha: float = 0.05) -> str:
    """
    https://zhuanlan.zhihu.com/p/112703276
    The Mann-Kendall test does not require samples to follow a certain distribution and is not disturbed by a few outliers. In the Mann-Kendall test, the null hypothesis is that H0 is the time series data (X1,... ,Xn), is a sample of n independent random variables equally distributed; The alternative hypothesis H1 is a two-sided test, and for all k, j≤n, and k≠j, the distribution of Xk and Xj is not the same. If the null hypothesis is unacceptable, there is a clear upward or downward trend in the time series data at the α confidence level. For statistic Z, if it is greater than 0, it is an upward trend; A value less than 0 indicates a downward trend
    :param x: 数据列表
    :param alpha: 置信度
    :return:
    """
    n = len(x)

    # calculate S
    s = 0
    for k in range(n - 1):
        for j in range(k + 1, n):
            s += np.sign(x[j] - x[k])

    # calculate the unique data
    unique_x, tp = np.unique(x, return_counts=True)
    g = len(unique_x)

    # calculate the var(s)
    if n == g:  # there is no tie
        var_s = (n * (n - 1) * (2 * n + 5)) / 18
    else:  # there are some ties in data
        var_s = (n * (n - 1) * (2 * n + 5) - np.sum(tp * (tp - 1) * (2 * tp + 5))) / 18

    if s > 0:
        z = (s - 1) / np.sqrt(var_s)
    elif s < 0:
        z = (s + 1) / np.sqrt(var_s)
    else:  # s == 0:
        z = 0

    # calculate the p_value
    p = 2 * (1 - norm.cdf(abs(z)))  # two tail test
    h = abs(z) > norm.ppf(1 - alpha / 2)

    if (z < 0) and h:
        trend = 'decreasing'
    elif (z > 0) and h:
        trend = 'increasing'
    else:
        trend = 'no trend'

    return "The trend of this keyword is " + trend
