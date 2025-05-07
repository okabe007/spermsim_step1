
"""run_sim.py – Step7, supports --num option"""
import argparse
import math
from core.simulation import SpermSimulation

DEFAULT_CONSTANTS = {
    'shape': 'cube',
    'radius': 1.0,
    'R': 1.0,
    'R_spot': 0.1,
    'drop_angle': math.radians(45),
    'theta_spot': math.radians(30),
    'step_length': 0.01,
    'n_simulation': 100,
    'number_of_sperm': 1,
    'deviation': 0.4,
}

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--shape', default='cube')
    p.add_argument('--volume', type=float, default=0.5)  # placeholder, not used here
    p.add_argument('--repeat', type=int, default=1)
    p.add_argument('--num', type=int, default=1, help='number of sperm')
    args = p.parse_args()

    constants = DEFAULT_CONSTANTS.copy()
    constants['shape'] = args.shape
    constants['number_of_sperm'] = args.num

    for r in range(args.repeat):
        sim = SpermSimulation(constants)
        sim.simulate()
        print(f'Run {r+1}: trajectory shape = {sim.trajectory.shape}')

if __name__ == '__main__':
    main()
