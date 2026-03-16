"""工具函数模块"""

"""工具函数模块"""

import json
import random
from typing import List, Dict, Any, Union, Tuple  # 需要添加 Tuple
from fractions import Fraction

def read_deck_from_file(filepath: str) -> List[str]:
    """从文件读取牌库"""
    with open(filepath, 'r', encoding='utf-8') as f:
        if filepath.endswith('.json'):
            data = json.load(f)
            if isinstance(data, list):
                return data
            elif isinstance(data, dict) and 'cards' in data:
                return data['cards']
        else:
            # 假设每行一张卡牌
            return [line.strip() for line in f if line.strip()]
    return []

def save_deck_to_file(deck: List[str], filepath: str):
    """保存牌库到文件"""
    with open(filepath, 'w', encoding='utf-8') as f:
        if filepath.endswith('.json'):
            json.dump({"cards": deck, "count": len(deck)}, f, indent=2, ensure_ascii=False)
        else:
            for card in deck:
                f.write(f"{card}\n")

def format_probability(prob: float, as_percent: bool = True, 
                        decimals: int = 2) -> str:
    """格式化概率显示"""
    if as_percent:
        return f"{prob * 100:.{decimals}f}%"
    return f"{prob:.{decimals}f}"

def format_fraction(prob: float) -> str:
    """将概率转换为分数形式"""
    f = Fraction(prob).limit_denominator(100)
    return f"{f.numerator}/{f.denominator}"

def shuffle_deck(deck: List[Any]) -> List[Any]:
    """洗牌"""
    shuffled = deck.copy()
    random.shuffle(shuffled)
    return shuffled

def draw_cards(deck: List[Any], count: int) -> Tuple[List[Any], List[Any]]:
    """抽牌，返回(抽到的牌, 剩余的牌)"""
    if count >= len(deck):
        return deck.copy(), []
    
    # 随机抽牌（不重复）
    indices = random.sample(range(len(deck)), count)
    drawn = [deck[i] for i in sorted(indices)]
    
    # 剩余的牌
    remaining = [deck[i] for i in range(len(deck)) if i not in indices]
    
    return drawn, remaining

def mana_curve(deck: List[Dict]) -> Dict[int, int]:
    """计算法力曲线"""
    curve = {}
    for card in deck:
        mana_cost = card.get('cost', 0)
        curve[mana_cost] = curve.get(mana_cost, 0) + 1
    return dict(sorted(curve.items()))

def average_mana_cost(deck: List[Dict]) -> float:
    """计算平均法力消耗"""
    if not deck:
        return 0.0
    
    total_cost = sum(card.get('cost', 0) for card in deck)
    return total_cost / len(deck)

def card_draw_simulator(deck: List[Any], draws: int, 
                          trials: int = 1000) -> Dict[str, float]:
    """抽牌模拟器"""
    results = {}
    
    for _ in range(trials):
        shuffled = shuffle_deck(deck)
        drawn = shuffled[:draws]
        
        for card in drawn:
            card_str = str(card)
            results[card_str] = results.get(card_str, 0) + 1
    
    # 转换为概率
    for card in results:
        results[card] /= trials
    
    return results