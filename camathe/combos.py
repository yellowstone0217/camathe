"""连击计算模块"""

import itertools
from typing import List, Tuple, Set, Dict, Any
from .core import CardMath

class ComboCalculator:
    """连击/组合计算类"""
    
    def __init__(self):
        self.cm = CardMath()
    
    def find_combinations(self, cards: List[Any], min_cards: int = 2,
                           max_cards: int = None) -> List[Tuple]:
        """
        找出所有可能的组合
        cards: 卡牌列表
        min_cards: 最小组合牌数
        max_cards: 最大组合牌数
        """
        if max_cards is None:
            max_cards = len(cards)
        
        max_cards = min(max_cards, len(cards))
        combinations = []
        
        for r in range(min_cards, max_cards + 1):
            combinations.extend(itertools.combinations(cards, r))
        
        return combinations
    
    def combo_power(self, combo: List[float], synergy_matrix: Dict[Tuple, float]) -> float:
        """
        计算组合强度
        combo: 组合中的卡牌数值列表
        synergy_matrix: 协同效应矩阵
        """
        base_power = sum(combo)
        synergy_bonus = 0.0
        
        # 计算所有卡牌对之间的协同效应
        for i, card1 in enumerate(combo):
            for j, card2 in enumerate(combo):
                if i < j:
                    synergy_bonus += synergy_matrix.get((card1, card2), 0)
                    synergy_bonus += synergy_matrix.get((card2, card1), 0)
        
        return base_power + synergy_bonus
    
    def optimal_combo(self, cards: List[float], synergy_matrix: Dict[Tuple, float],
                       max_cards: int = None) -> Tuple[List, float]:
        """
        找出最优组合
        """
        if max_cards is None:
            max_cards = len(cards)
        
        best_combo = []
        best_power = 0.0
        
        # 尝试所有可能的组合大小
        for size in range(2, min(max_cards, len(cards)) + 1):
            for combo in itertools.combinations(cards, size):
                power = self.combo_power(list(combo), synergy_matrix)
                if power > best_power:
                    best_power = power
                    best_combo = list(combo)
        
        return best_combo, best_power
    
    def chain_length(self, cards: List[Any], chain_rules: Dict[Any, List[Any]]) -> int:
        """
        计算可能的连击链长度
        cards: 可用卡牌
        chain_rules: 连击规则，格式 {卡牌: [可以连击的卡牌列表]}
        """
        max_chain = 0
        
        for start_card in cards:
            used = {start_card}
            current = start_card
            chain = 1
            
            while True:
                next_options = [c for c in chain_rules.get(current, []) 
                               if c in cards and c not in used]
                if not next_options:
                    break
                
                current = next_options[0]  # 简单选择第一个
                used.add(current)
                chain += 1
            
            max_chain = max(max_chain, chain)
        
        return max_chain
    
    def combo_count(self, deck: List[Any], combo_requirements: List[Set]) -> int:
        """
        计算牌库中可能组成多少种特定组合
        deck: 牌库
        combo_requirements: 组合要求列表，每个要求是一组需要的卡牌
        """
        deck_counter = {}
        for card in deck:
            deck_counter[card] = deck_counter.get(card, 0) + 1
        
        possible_combos = 0
        for requirement in combo_requirements:
            # 检查是否满足所有要求
            satisfied = True
            combo_count = 1
            
            for card in requirement:
                if deck_counter.get(card, 0) == 0:
                    satisfied = False
                    break
                combo_count *= deck_counter[card]
            
            if satisfied:
                possible_combos += combo_count
        
        return possible_combos