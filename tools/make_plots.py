"""
make_plots.py
Usage example:
    python tools/make_plots.py traj.npy --shape cube --const const.json
"""

import argparse, json, numpy as np, os, sys
import plot_utils as pu

p = argparse.ArgumentParser()
p.add_argument("traj_file", help=".npy saved trajectory (n_step,3)")
p.add_argument("--shape", required=True, choices=("cube", "drop", "spot"))
p.add_argument("--const", help="constants JSON")
p.add_argument("--png", default="traj2d.png")
p.add_argument("--movie", default="traj3d.mp4")
args = p.parse_args()

traj = np.load(args.traj_file)
const = json.load(open(args.const)) if args.const else {}

pu.plot_2d(traj, args.shape, const, fname=args.png)
pu.animate_3d(traj, args.shape, const, fname=args.movie)
print("Saved:", args.png, "and", args.movie)
