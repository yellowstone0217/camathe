"""核心数学函数"""

import math
from fractions import Fraction
from typing import Union, List, Tuple

class CardMath:
    """卡牌数学计算核心类"""
    
    @staticmethod
    def combo(n: int, k: int) -> int:
        """计算组合数 C(n, k)"""
        if k < 0 or k > n:
            return 0
        return math.comb(n, k)
    
    @staticmethod
    def perm(n: int, k: int) -> int:
        """计算排列数 P(n, k)"""
        if k < 0 or k > n:
            return 0
        return math.perm(n, k)
    
    @staticmethod
    def factorial(n: int) -> int:
        """计算阶乘"""
        return math.factorial(n)
    
    @staticmethod
    def hypergeom(k: int, n: int, K: int, N: int) -> float:
        """
        超几何分布概率
        从N个中抽n个，其中K个成功，求恰好抽到k个成功的概率
        """
        if k < 0 or k > min(n, K):
            return 0.0
        return (math.comb(K, k) * math.comb(N - K, n - k)) / math.comb(N, n)
    
    def hypergeom_cumulative(self, k: int, n: int, K: int, N: int, 
                              lower_tail: bool = True) -> float:
        """超几何分布累积概率"""
        if lower_tail:
            return sum(self.hypergeom(i, n, K, N) for i in range(k + 1))
        else:
            return sum(self.hypergeom(i, n, K, N) for i in range(k, min(n, K) + 1))
    
    @staticmethod
    def expected_value(values: List[float], probs: List[float]) -> float:
        """计算期望值"""
        return sum(v * p for v, p in zip(values, probs))
    
    @staticmethod
    def variance(values: List[float], probs: List[float]) -> float:
        """计算方差"""
        mean = CardMath.expected_value(values, probs)
        return sum(p * (v - mean) ** 2 for v, p in zip(values, probs))
    
    def double(self, x: Union[int, float, List]) -> Union[int, float, List]:
        """快速增加双数 - 核心功能"""
        if isinstance(x, (int, float)):
            return x * 2
        elif isinstance(x, list):
            return [self.double(i) for i in x]
        else:
            raise TypeError(f"不支持的类型: {type(x)}")
    
    def half(self, x: Union[int, float, List]) -> Union[int, float, List]:
        """快速减半"""
        if isinstance(x, (int, float)):
            return x / 2
        elif isinstance(x, list):
            return [self.half(i) for i in x]
        else:
            raise TypeError(f"不支持的类型: {type(x)}")
    
    def damage_range(self, base: int, modifiers: List[float]) -> Tuple[float, float]:
        """计算伤害范围"""
        min_dmg = base * min(modifiers)
        max_dmg = base * max(modifiers)
        return (min_dmg, max_dmg)