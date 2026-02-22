import os

# Web版ではファイル保存をせず、このリスト（メモリ）に保存する
_memory_scores = []

def update_ranking(new_score):
    global _memory_scores
    
    # 1. 前回のスコアリストに今回のスコアを追加
    _memory_scores.append(new_score)
    
    # 2. 大きい順に並べ替えて、上位5つだけ残す
    _memory_scores.sort(reverse=True)
    top_five = _memory_scores[:5]
    
    # ★重要：Web版では open(...) による書き込み処理を消します！
    # これを入れるとブラウザでエラーになり、画面が止まります。
    
    return top_five

def get_ranking():
    global _memory_scores
    return _memory_scores
