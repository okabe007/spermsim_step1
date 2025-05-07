"""
plot_utils.py
2D / 3D visualization utilities for sperm simulation.
Colors:
  - Medium   : pink  (#ffc0cb)
  - Egg      : yellow (#ffd700)
  - Boundary : grey  (#808080)
  - Hit step : red   (#ff0000, lw=3)
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, writers
from mpl_toolkits.mplot3d import Axes3D  # noqa F401

PINK   = "#ffc0cb"
YELLOW = "#ffd700"
GREY   = "#808080"
RED    = "#ff0000"


# ---------- helpers -----------------------------------------------------------
def _inside(pt, shape, c):
    if shape == "cube":
        return np.all(np.abs(pt) <= c["radius"])
    if shape == "drop":
        return np.linalg.norm(pt) <= c["R"]
    if shape == "spot":
        return np.linalg.norm(pt) <= c["R_spot"]
    return False


# ----------------------- 2D ---------------------------------------------------
def _egg_patch(shape, c, ax):
    if shape == "cube":
        r = c["radius"]
        ax.add_patch(plt.Rectangle((-r, -r), 2 * r, 2 * r,
                                   facecolor=YELLOW, edgecolor=GREY, alpha=.3))
    else:                               # drop / spot → 円
        R = c["R"] if shape == "drop" else c["R_spot"]
        circ = plt.Circle((0, 0), R, facecolor=YELLOW,
                          edgecolor=GREY, alpha=.3)
        ax.add_patch(circ)


def plot_2d(traj, shape, c, fname="traj2d.png"):
    """
    traj : (n_step, 3)
    保存先 fname は PNG 推奨
    """
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.set_aspect("equal")
    ax.set_facecolor(PINK)
    _egg_patch(shape, c, ax)

    ax.plot(traj[:, 0], traj[:, 1], color="k", lw=.8)
    for i in range(len(traj) - 1):
        if _inside(traj[i + 1], shape, c):
            p, q = traj[i], traj[i + 1]
            ax.plot([p[0], q[0]], [p[1], q[1]], color=RED, lw=3)
    ax.set_title("2D trajectory")
    plt.savefig(fname, dpi=150)
    plt.close()


# ----------------------- 3D ---------------------------------------------------
def _cube_wire(ax, r):
    s = [-r, r]
    for x in s:
        for y in s:
            ax.plot([x, x], [y, y], [-r, r], c=GREY, alpha=.6)
    for x in s:
        for z in s:
            ax.plot([x, x], [-r, r], [z, z], c=GREY, alpha=.6)
    for y in s:
        for z in s:
            ax.plot([-r, r], [y, y], [z, z], c=GREY, alpha=.6)


def _sphere_wire(ax, R):
    u = np.linspace(0, 2 * np.pi, 30)
    v = np.linspace(0, np.pi, 15)
    for vv in v:
        ax.plot(R * np.cos(u) * np.sin(vv),
                R * np.sin(u) * np.sin(vv),
                R * np.full_like(u, np.cos(vv)),
                c=GREY, alpha=.5)
    for uu in u:
        ax.plot(R * np.full_like(v, np.cos(uu)),
                R * np.sin(v) * np.sin(uu),
                R * np.cos(v),
                c=GREY, alpha=.5)


def animate_3d(traj, shape, c, fname="traj3d.mp4", fps=20):
    fig = plt.figure(figsize=(5, 5))
    ax = fig.add_subplot(111, projection="3d")
    ax.set_facecolor(PINK)

    if shape == "cube":
        _cube_wire(ax, c["radius"])
    else:
        R = c["R"] if shape == "drop" else c["R_spot"]
        _sphere_wire(ax, R)

    line, = ax.plot([], [], [], c="k", lw=.8)
    hit,  = ax.plot([], [], [], c=RED, lw=3)
    lim = 0.12
    ax.set(xlim=(-lim, lim), ylim=(-lim, lim), zlim=(-lim, lim))

    def update(i):
        line.set_data(traj[:i + 1, 0], traj[:i + 1, 1])
        line.set_3d_properties(traj[:i + 1, 2])
        if _inside(traj[i], shape, c):
            hit.set_data(traj[i - 1:i + 1, 0], traj[i - 1:i + 1, 1])
            hit.set_3d_properties(traj[i - 1:i + 1, 2])
        return line, hit

    ani = FuncAnimation(fig, update, frames=len(traj), blit=True)
    ani.save(fname, writer=writers["ffmpeg"](fps=fps))
    plt.close()
