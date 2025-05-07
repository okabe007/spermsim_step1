"""core/geometry.py – Drop/Spot wall normal & compat helpers"""
from __future__ import annotations
import numpy as np, math
from enum import Enum, auto

class IOStatus(Enum):
    INSIDE = auto()
    SURFACE = auto()
    OUTSIDE = auto()
    BORDER = auto()
    TEMP_SURFACE = auto()
    TEMP_EDGE = auto()
    STICK_SURFACE = auto()

# ------------ vector helpers -----------------
def random_unit_vector() -> np.ndarray:
    phi = np.random.uniform(0, 2*math.pi)
    costh = np.random.uniform(-1, 1)
    sinth = math.sqrt(1 - costh*costh)
    return np.array([sinth*math.cos(phi), sinth*math.sin(phi), costh])

def initial_vec(constants: dict) -> np.ndarray:
    """旧仕様との互換：ランダム方向 × step_length"""
    return random_unit_vector() * constants['step_length']

# ------------- random initial points ----------
def random_point_cube(r: float) -> np.ndarray:
    return np.random.uniform(-r, r, 3)

def _rand_in_sphere(R: float) -> np.ndarray:
    while True:
        p = np.random.uniform(-R, R, 3)
        if p @ p <= R*R:
            return p

def random_point_cap(R: float, theta: float) -> np.ndarray:
    zc = R*math.cos(theta)
    while True:
        p = _rand_in_sphere(R)
        if p[2] >= 0 and (p[2]-zc) >= -1e-9:
            return p

# ---------------- IO checks -------------------
def IO_check_cube(p0, p1, c):
    R = c['radius']
    abs1 = np.abs(p1)
    if np.all(abs1 < R): return IOStatus.INSIDE
    if np.any(np.isclose(abs1, R, atol=1e-9)): return IOStatus.TEMP_SURFACE
    return IOStatus.OUTSIDE

def IO_check_drop(p0, p1, c):
    R = c['R']; theta = c['drop_angle']; zc = R*math.cos(theta)
    if p1[2] < 0: return IOStatus.OUTSIDE
    dist2 = np.sum((p1 - np.array([0,0,zc]))**2)
    if dist2 < R*R - 1e-9: return IOStatus.INSIDE
    if abs(dist2 - R*R) <= 1e-9: return IOStatus.TEMP_SURFACE
    return IOStatus.OUTSIDE

def IO_check_spot(p0, p1, c):
    R = c['R_spot']
    theta = c.get('theta_spot', math.pi/6)      # fallback
    zc = R*math.cos(theta)
    if p1[2] < 0: return IOStatus.OUTSIDE
    dist2 = np.sum((p1 - np.array([0,0,zc]))**2)
    if dist2 < R*R - 1e-9: return IOStatus.INSIDE
    if abs(dist2 - R*R) <= 1e-9: return IOStatus.TEMP_SURFACE
    return IOStatus.OUTSIDE

# ------------- normals for first hit ----------
def first_hit_normal_cube(p0, p1, R):
    if np.all(np.abs(p1) < R): return None
    for ax in range(3):
        if abs(p1[ax]) >= R - 1e-12:
            n = np.zeros(3); n[ax] = np.sign(p1[ax]); return n
    return None

def first_hit_normal_drop(p0, p1, R, theta):
    if p1[2] < 0: return np.array([0,0,-1])
    c = np.array([0,0,R*math.cos(theta)])
    v = p1 - c
    dist = np.linalg.norm(v)
    if dist >= R - 1e-12:
        return v / dist
    return None

def first_hit_normal_spot(p0, p1, R, theta):
    if p1[2] < 0: return np.array([0,0,-1])
    c = np.array([0,0,R*math.cos(theta)])
    v = p1 - c
    dist = np.linalg.norm(v)
    if dist >= R - 1e-12:
        return v / dist
    return None

# -------------- prepare & resolve -------------
def prepare_new_vector(last_vec, c, boundary_type="free", stick_status:int=0, inward_dir=None):
    step = c['step_length']
    if stick_status > 0 and inward_dir is not None:
        n = inward_dir / np.linalg.norm(inward_dir)
        tang = last_vec - np.dot(last_vec, n)*n
        if np.linalg.norm(tang) < 1e-12:
            tang = np.cross(n, [1,0,0])
            if np.linalg.norm(tang) < 1e-12:
                tang = np.cross(n, [0,1,0])
        tang = tang / np.linalg.norm(tang)
        return tang * step
    dev = c.get('deviation', 0.4)
    rand = random_unit_vector()
    new = (1-dev)*last_vec + dev*rand
    new /= np.linalg.norm(new)
    return new * step

def resolve_step(p_curr, v_raw, c):
    step = c['step_length']
    remaining = v_raw.copy()
    start = p_curr.copy()
    p = p_curr.copy()
    for _ in range(3):
        shape = c['shape']
        if shape == 'cube':
            n = first_hit_normal_cube(p, p+remaining, c['radius'])
        elif shape == 'drop':
            n = first_hit_normal_drop(p, p+remaining, c['R'], c['drop_angle'])
        elif shape == 'spot':
            n = first_hit_normal_spot(p, p+remaining, c['R_spot'], c.get('theta_spot', math.pi/6))
        else:
            n = None
        if n is None:
            return start + v_raw - start
        tang = remaining - np.dot(remaining, n)*n
        if np.linalg.norm(tang) < 1e-12: break
        tang = tang / np.linalg.norm(tang) * step
        p = p + tang
        remaining = start + v_raw - p
    return p - start
