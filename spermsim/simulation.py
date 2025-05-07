"""simulation.py – Step3b: クラスラッパー導入

既存 repeat_simulation() を内部で呼ぶだけの `SpermSimulation` クラスを追加。
将来的に本体ロジックをこちらへ移植していく。
"""
from __future__ import annotations
from typing import Dict, Any, List, Tuple

class SpermSimulation:
    """計算エンジンの薄ラッパー"""

    def __init__(self, constants: Dict[str, Any], shape):
        self.constants = constants
        self.shape = shape   # geometry.Shape インスタンス

    def run(self, n_repeat: int):
        """既存実装を遅延 import して呼び出すだけ"""
        from spermsim.main import repeat_simulation as _orig_rep
        # 今は shape を使っていないが、後続ステップで利用予定
        return _orig_rep(self.constants, n_repeat)