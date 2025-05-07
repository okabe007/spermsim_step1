"""
simulation.py  ―  Step3 修正版（循環 import 回避）

今は旧 `main.repeat_simulation` を **呼び出すだけ** の薄ラッパー。
"""

from __future__ import annotations
from typing import Dict, Any


def repeat_simulation(constants: Dict[str, Any], n_repeat: int):
    """元の実装を遅延 import して呼び出す"""
    from spermsim.main import repeat_simulation as _orig_rep
    return _orig_rep(constants, n_repeat)
