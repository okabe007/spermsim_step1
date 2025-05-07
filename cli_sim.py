
"""cli_sim.py
Run sperm simulation core with parameters from a YAML config file.

Usage:
    python cli_sim.py config/example.yaml
    # or default
    python cli_sim.py

YAML example keys (all optional, defaults shown):
    shape: cube          # cube | drop | spot
    radius: 1.0
    R: 1.0               # drop
    drop_angle_deg: 45
    R_spot: 0.1          # spot
    theta_spot_deg: 30
    H_spot: 0.1
    step_length: 0.01
    n_simulation: 100
    number_of_sperm: 1
    deviation: 0.4
    repeat: 3
"""

import argparse
import math
import sys
from pathlib import Path

import yaml
import numpy as np

from core.simulation import SpermSimulation

DEFAULT_CONFIG = {
    'shape': 'cube',
    'radius': 1.0,
    'R': 1.0,
    'drop_angle_deg': 45,
    'R_spot': 0.1,
    'theta_spot_deg': 30,
    'H_spot': 0.1,
    'step_length': 0.01,
    'n_simulation': 100,
    'number_of_sperm': 1,
    'deviation': 0.4,
    'repeat': 3,
}

def load_config(path: Path | None):
    if path is None:
        return DEFAULT_CONFIG.copy()
    data = yaml.safe_load(path.read_text())
    cfg = DEFAULT_CONFIG.copy()
    cfg.update(data or {})
    return cfg

def to_constants(cfg: dict):
    c = cfg.copy()
    # degree → rad
    c['drop_angle'] = math.radians(c.get('drop_angle_deg', 45))
    c['theta_spot'] = math.radians(c.get('theta_spot_deg', 30))
    # ensure required keys
    return c

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('config', nargs='?', type=str, help='YAML config path')
    args = parser.parse_args()

    cfg = load_config(Path(args.config) if args.config else None)
    repeat = cfg.pop('repeat', 1)
    constants = to_constants(cfg)

    for r in range(repeat):
        sim = SpermSimulation(constants)
        sim.simulate()
        first = sim.trajectory[0]
        print(f'Run {r+1}: first 5 coords = {first[:5]}')

if __name__ == '__main__':
    main()
