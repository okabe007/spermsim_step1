from __future__ import annotations
from core.db import save_run_meta, save_summary, save_contacts
import numpy as np, math
from core.geometry import (
    prepare_new_vector, resolve_step,
    random_point_cube, random_point_cap
)

# ───────────────── inside_egg ───────────────────
def inside_egg(p: np.ndarray, c: dict) -> bool:
    """
    非常に単純な内部判定。
    形状別の IO_check_* が既にある場合は差し替えてください。
    """
    s = c['shape']
    if s == 'cube':
        return np.all(np.abs(p) <= c['radius'])
    elif s == 'drop':
        return np.linalg.norm(p) <= c['R']
    elif s == 'spot':
        return np.linalg.norm(p) <= c['R_spot']
    return False

# ───────────────── シミュレーションクラス ───────────────────
class SpermSimulation:
    def __init__(self, c: dict):
        self.c = c
        self.n_sperm = int(c.get('number_of_sperm', 1))
        self.n_step  = int(c.get('n_simulation', 100))
        self.traj = np.zeros((self.n_sperm, self.n_step, 3))
        self.trajectory = self.traj

    # ---- 初期位置 ------------------------------------------------
    def _init_pos(self) -> np.ndarray:
        s = self.c['shape']
        if s == 'cube':
            return random_point_cube(self.c['radius'])
        elif s == 'drop':
            return random_point_cap(self.c['R'], self.c['drop_angle'])
        elif s == 'spot':
            return random_point_cap(
                self.c['R_spot'],
                self.c.get('theta_spot', math.pi / 6)
            )
        return np.zeros(3)

    # ---- メイン ---------------------------------------------------
    def simulate(self):
        step_len = self.c['step_length']
        last_vec = np.array([step_len, 0.0, 0.0])

        dt_sec = 4.0  # 1 step = 4 秒 (必要なら変更)
        contacts = []  # (idx, step, t_sec, x, y, z)

        # 1. 初期化
        for i in range(self.n_sperm):
            self.traj[i, 0] = self._init_pos()
        start_t = 1

        # 2. メインループ
        for t in range(start_t, self.n_step):
            for i in range(self.n_sperm):
                pos = self.traj[i, t - 1]
                v_raw = prepare_new_vector(last_vec, self.c)
                v = resolve_step(pos, v_raw, self.c)
                newp = pos + v
                self.traj[i, t] = newp
                if inside_egg(newp, self.c):
                    contacts.append((i, t, t * dt_sec, *newp))
            last_vec = self.traj[0, t] - self.traj[0, t - 1]

        # 3. DB へ保存
        run_id = save_run_meta(self.c)
        save_summary(run_id, len(contacts))
        if contacts:
            save_contacts(run_id, contacts)

        return self.traj
