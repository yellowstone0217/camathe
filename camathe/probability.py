"""概率计算模块"""

import random
from typing import List, Tuple, Dict, Any, Optional
from collections import Counter
from .core import CardMath

class Probability:
    """概率计算类"""
    
    def __init__(self):
        self.cm = CardMath()
    
    def draw_probability(self, deck_size: int, target_cards: int, 
                          draws: int, want: int) -> float:
        """
        计算抽到特定数量目标卡牌的概率
        deck_size: 牌库总数
        target_cards: 目标卡牌数量
        draws: 抽牌数量
        want: 想要抽到的数量
        """
        if want > draws or want > target_cards:
            return 0.0
        return self.cm.hypergeom(want, draws, target_cards, deck_size)
    
    def draw_at_least(self, deck_size: int, target_cards: int, 
                       draws: int, at_least: int) -> float:
        """计算至少抽到特定数量目标卡牌的概率"""
        return self.cm.hypergeom_cumulative(
            at_least, draws, target_cards, deck_size, lower_tail=False
        )
    
    def combo_probability(self, deck: Dict[str, int], 
                           combo_cards: List[str], draws: int) -> float:
        """
        计算在特定牌库中抽到特定组合的概率
        deck: 牌库，格式 {"卡牌名称": 数量}
        combo_cards: 需要的卡牌列表
        draws: 抽牌数量
        """
        total_cards = sum(deck.values())
        needed_unique = len(combo_cards)
        
        if draws < needed_unique:
            return 0.0
        
        # 简化计算 - 假设每张需要的卡牌至少抽到1张
        prob = 1.0
        remaining_deck = total_cards
        remaining_draws = draws
        
        for card in combo_cards:
            card_count = deck.get(card, 0)
            if card_count == 0:
                return 0.0
            
            # 计算抽到这张卡的概率（近似）
            p = self.draw_at_least(remaining_deck, card_count, remaining_draws, 1)
            prob *= p
            
            # 更新剩余牌库（简化处理）
            remaining_deck -= 1
            remaining_draws -= 1
            
        return prob
    
    def simulate_draws(self, deck: List[Any], draws: int, 
                        trials: int = 10000) -> Dict[Any, float]:
        """
        通过模拟计算抽牌分布
        deck: 牌库列表
        draws: 抽牌数量
        trials: 模拟次数
        """
        results = []
        
        for _ in range(trials):
            sample = random.sample(deck, min(draws, len(deck)))
            results.extend(sample)
        
        counter = Counter(results)
        return {item: count / trials for item, count in counter.items()}
    
    def mulligan_probability(self, deck_size: int, target_cards: int,
                               initial_hand: int, mulligan_draws: int) -> float:
        """
        计算调度后的概率（简单版本）
        """
        # 第一次抽牌概率
        p_initial = self.draw_at_least(deck_size, target_cards, initial_hand, 1)
        
        # 如果没抽到，调度后重新抽的概率
        p_mulligan = self.draw_at_least(deck_size, target_cards, mulligan_draws, 1)
        
        # 总概率
        return p_initial + (1 - p_initial) * p_mulligan