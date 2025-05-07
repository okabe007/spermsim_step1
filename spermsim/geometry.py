
"""geometry.py  –  Step2 形状クラス薄ラッパー
現状 main.py 内の形状依存関数 (IO_check_xxx) をクラス化するための土台。
まずは既存関数をそのまま呼び出すだけに留め、挙動を変えません。
本ファイルを spermsim/ フォルダに置き、main.py から:
    from geometry import create_shape
で Shape インスタンスを生成して利用してください。
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Any, Tuple, Protocol


# ---------- インタフェース ---------- #
class Shape(Protocol):
    name: str

    def get_limits(self) -> Tuple[float, float, float, float, float, float]:
        ...

    def io_check(self, x: float, y: float, z: float) -> str:
        ...

    def initial_position(self) -> Tuple[float, float, float]:
        ...


# ---------- 共通親 ---------- #
@dataclass
class BaseShape:
    constants: Dict[str, Any]

    def get_limits(self):
        raise NotImplementedError

    def io_check(self, x, y, z):
        raise NotImplementedError

    def initial_position(self):
        raise NotImplementedError


# ---------- 各 Shape 薄ラッパー ---------- #
class CubeShape(BaseShape):
    name = "cube"

    def get_limits(self):
        from .main import get_limits_cube
        return get_limits_cube(self.constants)

    def io_check(self, x, y, z):
        from .main import IO_check_cube
        return IO_check_cube(x, y, z, self.constants)

    def initial_position(self):
        from .main import initial_position_cube
        return initial_position_cube(self.constants)


class DropShape(BaseShape):
    name = "drop"

    def get_limits(self):
        from .main import get_limits_drop
        return get_limits_drop(self.constants)

    def io_check(self, x, y, z):
        from .main import IO_check_drop
        return IO_check_drop(x, y, z, self.constants)

    def initial_position(self):
        from .main import initial_position_drop
        return initial_position_drop(self.constants)


class SpotShape(BaseShape):
    name = "spot"

    def get_limits(self):
        from .main import get_limits_spot
        return get_limits_spot(self.constants)

    def io_check(self, x, y, z):
        from .main import IO_check_spot
        return IO_check_spot(x, y, z, self.constants)

    def initial_position(self):
        from .main import initial_position_spot
        return initial_position_spot(self.constants)


class CerosShape(BaseShape):
    name = "ceros"

    def get_limits(self):
        from .main import get_limits_ceros
        return get_limits_ceros(self.constants)

    def io_check(self, x, y, z):
        from .main import IO_check_ceros
        return IO_check_ceros(x, y, z, self.constants)

    def initial_position(self):
        from .main import initial_position_ceros
        return initial_position_ceros(self.constants)


# ---------- Factory ---------- #
def create_shape(shape_name: str, constants: Dict[str, Any]) -> Shape:
    shape_map = {
        "cube": CubeShape,
        "drop": DropShape,
        "spot": SpotShape,
        "ceros": CerosShape,
    }
    try:
        return shape_map[shape_name.lower()](constants)
    except KeyError:
        raise ValueError(f"Unknown shape '{shape_name}'. Available: {list(shape_map)}")
