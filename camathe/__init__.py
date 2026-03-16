"""
camathe - 卡牌游戏计算库
一个对卡牌游戏非常良心的库，快速计算数字
"""

from camathe.core import CardMath
from camathe.probability import Probability
from camathe.combos import ComboCalculator
from camathe.damage import DamageCalculator
from camathe.utils import *

__version__ = "0.1.0"
__author__ = "Your Name"

# 创建便捷的实例供直接使用
cm = CardMath()
prob = Probability()
combo = ComboCalculator()
dmg = DamageCalculator()

__all__ = [
    "CardMath",
    "Probability",
    "ComboCalculator",
    "DamageCalculator",
    "cm",
    "prob",
    "combo",
    "dmg",
]