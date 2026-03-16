"""伤害计算模块"""

import math
from typing import List, Tuple, Dict, Union, Optional

class DamageCalculator:
    """伤害计算类"""
    
    def __init__(self):
        self.damage_modifiers = {}
        self.critical_multiplier = 2.0
    
    def calculate(self, base_damage: float, 
                   modifiers: List[Tuple[str, float]] = None) -> float:
        """
        计算最终伤害
        base_damage: 基础伤害
        modifiers: 修正列表，格式 [("add", 10), ("multiply", 1.5)]
        """
        if modifiers is None:
            modifiers = []
        
        damage = base_damage
        
        for mod_type, value in modifiers:
            if mod_type == "add":
                damage += value
            elif mod_type == "subtract":
                damage -= value
            elif mod_type == "multiply":
                damage *= value
            elif mod_type == "divide":
                damage /= value if value != 0 else 1
            elif mod_type == "percent_add":
                damage *= (1 + value / 100)
            elif mod_type == "percent_subtract":
                damage *= (1 - value / 100)
        
        return max(0, damage)  # 伤害不能为负
    
    def with_critical(self, base_damage: float, critical_rate: float,
                       critical_damage: float = None) -> Tuple[float, float]:
        """
        计算暴击伤害
        base_damage: 基础伤害
        critical_rate: 暴击率 (0-1)
        critical_damage: 暴击伤害倍率
        """
        if critical_damage is None:
            critical_damage = self.critical_multiplier
        
        # 期望伤害
        expected = base_damage * (1 + critical_rate * (critical_damage - 1))
        
        # 最大可能伤害
        max_damage = base_damage * critical_damage
        
        return expected, max_damage
    
    def chain_damage(self, base_damage: float, chain_count: int,
                       chain_multiplier: float = 1.2) -> List[float]:
        """
        计算连击伤害
        chain_count: 连击次数
        chain_multiplier: 每次连击的倍率
        """
        damages = []
        current = base_damage
        
        for i in range(chain_count):
            damages.append(current)
            current *= chain_multiplier
        
        return damages
    
    def aoe_damage(self, base_damage: float, target_count: int,
                    falloff: float = 1.0) -> List[float]:
        """
        计算范围伤害
        target_count: 目标数量
        falloff: 衰减系数 (1.0 = 无衰减, 0.5 = 每多一个目标减少50%)
        """
        damages = []
        
        for i in range(target_count):
            if i == 0:
                damages.append(base_damage)
            else:
                multiplier = falloff ** i
                damages.append(base_damage * multiplier)
        
        return damages
    
    def kill_threshold(self, base_damage: float, enemy_hp: float,
                        armor: float = 0) -> Tuple[bool, int]:
        """
        计算是否能击杀及所需攻击次数
        base_damage: 每次攻击伤害
        enemy_hp: 敌人生命值
        armor: 敌人护甲
        """
        actual_damage = max(0, base_damage - armor)
        
        if actual_damage <= 0:
            return False, float('inf')
        
        hits_needed = math.ceil(enemy_hp / actual_damage)
        return True, hits_needed
    
    def damage_over_time(self, base_damage: float, duration: int,
                          interval: int = 1, tick_multiplier: float = 1.0) -> float:
        """
        计算持续伤害总量
        base_damage: 每跳基础伤害
        duration: 持续时间
        interval: 伤害间隔
        tick_multiplier: 每跳倍率
        """
        ticks = duration // interval
        total = 0
        
        for tick in range(ticks):
            # 有些游戏持续伤害会衰减或递增
            multiplier = tick_multiplier ** tick
            total += base_damage * multiplier
        
        return total
    
    def combo_damage(self, combo_cards: List[Dict], 
                      combo_bonus: Dict[Tuple, float]) -> float:
        """
        计算组合伤害
        combo_cards: 组合中的卡牌，每张卡牌格式 {"damage": 100, "type": "fire"}
        combo_bonus: 组合加成
        """
        total = 0
        card_types = []
        
        # 基础伤害
        for card in combo_cards:
            total += card.get("damage", 0)
            card_types.append(card.get("type", "normal"))
        
        # 组合加成
        for i, type1 in enumerate(card_types):
            for j, type2 in enumerate(card_types):
                if i < j:
                    bonus = combo_bonus.get((type1, type2), 0)
                    total += bonus
        
        return total