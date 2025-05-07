#!/usr/bin/env python3
"""
Sperm Simulation GUI v3
──────────────────────────────────────────
┌ Parameters ┐┌ History ┐ の 2タブ構成
* Parameters : 既存入力 → Run Simulation
* History    : 実行履歴一覧 → Histogram / Refresh
"""
from __future__ import annotations
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3, json, pathlib, subprocess, math

from core.simulation import SpermSimulation
from core.db import save_figure, DB_PATH

TOOLS_DIR  = pathlib.Path(__file__).resolve().parent / "tools"
ANZ_SCRIPT = TOOLS_DIR / "analyze.py"

# ───────────────── DB helper ──────────────────
def list_runs(limit: int = 200):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.execute(
        "SELECT run_id,shape,created FROM runs ORDER BY run_id DESC LIMIT ?",
        (limit,))
    rows = cur.fetchall()
    conn.close()
    return rows

# ───────────────── GUI class ───────────────────
class SimApp(ttk.Notebook):            # Notebook 継承 → タブ UI
    def __init__(self):
        root = tk.Tk()
        super().__init__(root)
        root.title("Sperm Simulation GUI v3")
        root.geometry("540x420")

        self.make_param_tab()
        self.make_history_tab()

        self.pack(expand=1, fill="both")
        root.mainloop()

    # ---------- Parameters tab -----------------
    def make_param_tab(self):
        tab = ttk.Frame(self)
        self.add(tab, text="Parameters")
        r = 0

        def lbl(text):
            ttk.Label(tab, text=text).grid(row=r, column=0, sticky="e")

        lbl("Shape")
        self.shape = tk.StringVar(value="cube")
        ttk.Combobox(tab, textvariable=self.shape,
                     values=("cube", "drop", "spot"), width=8
                     ).grid(row=r, column=1, sticky="w")
        r += 1

        lbl("Radius (cube)")
        self.radius = tk.StringVar(value="1.0")
        tk.Entry(tab, textvariable=self.radius, width=8
                 ).grid(row=r, column=1, sticky="w"); r += 1

        lbl("Step length")
        self.step = tk.StringVar(value="0.01")
        tk.Entry(tab, textvariable=self.step, width=8
                 ).grid(row=r, column=1, sticky="w"); r += 1

        lbl("n_simulation")
        self.nsim = tk.StringVar(value="200")
        tk.Entry(tab, textvariable=self.nsim, width=8
                 ).grid(row=r, column=1, sticky="w"); r += 1

        lbl("Deviation")
        self.dev = tk.StringVar(value="0.4")
        tk.Entry(tab, textvariable=self.dev, width=8
                 ).grid(row=r, column=1, sticky="w"); r += 1

        lbl("Repeat")
        self.repeat = tk.StringVar(value="1")
        tk.Entry(tab, textvariable=self.repeat, width=8
                 ).grid(row=r, column=1, sticky="w"); r += 1

        # --- Drop params ---
        ttk.Label(tab, text="--- Drop params ---"
                  ).grid(row=r, columnspan=2, pady=2); r += 1
        lbl("R")
        self.drop_R = tk.StringVar(value="1.0")
        tk.Entry(tab, textvariable=self.drop_R, width=8
                 ).grid(row=r, column=1, sticky="w"); r += 1
        lbl("Angle deg")
        self.drop_ang = tk.StringVar(value="45")
        tk.Entry(tab, textvariable=self.drop_ang, width=8
                 ).grid(row=r, column=1, sticky="w"); r += 1

        # --- Spot params ---
        ttk.Label(tab, text="--- Spot params ---"
                  ).grid(row=r, columnspan=2, pady=2); r += 1
        lbl("R_spot")
        self.spot_R = tk.StringVar(value="0.1")
        tk.Entry(tab, textvariable=self.spot_R, width=8
                 ).grid(row=r, column=1, sticky="w"); r += 1
        lbl("Theta deg")
        self.spot_theta = tk.StringVar(value="30")
        tk.Entry(tab, textvariable=self.spot_theta, width=8
                 ).grid(row=r, column=1, sticky="w"); r += 1
        lbl("H_spot")
        self.spot_H = tk.StringVar(value="0.1")
        tk.Entry(tab, textvariable=self.spot_H, width=8
                 ).grid(row=r, column=1, sticky="w"); r += 1

        ttk.Button(tab, text="Run Simulation",
                   command=self.run_sim).grid(row=r, columnspan=2, pady=10)

    def build_constants(self):
        try:
            step = float(self.step.get())
            n = int(self.nsim.get())
            dev = float(self.dev.get())
        except ValueError as e:
            messagebox.showerror("Input err", str(e))
            return None

        c = {'shape': self.shape.get(),
             'step_length': step,
             'n_simulation': n,
             'deviation': dev,
             'number_of_sperm': 1}

        if c['shape'] == "cube":
            c['radius'] = float(self.radius.get())

        elif c['shape'] == "drop":
            R = float(self.drop_R.get())
            theta = math.radians(float(self.drop_ang.get()))
            c.update(R=R, drop_angle=theta)

        elif c['shape'] == "spot":
            R = float(self.spot_R.get())
            theta = math.radians(float(self.spot_theta.get()))
            c.update(R_spot=R, theta_spot=theta,
                     H_spot=float(self.spot_H.get()))
        return c

    def run_sim(self):
        c = self.build_constants()
        if c is None:
            return
        rep = int(self.repeat.get())
        for _ in range(rep):
            sim = SpermSimulation(c)
            sim.simulate()
        messagebox.showinfo("Done", f"Ran {rep} times.")
        self.refresh_runs()

    # ---------- History tab -------------------
    def make_history_tab(self):
        tab = ttk.Frame(self)
        self.add(tab, text="History")

        self.tree = ttk.Treeview(
            tab, columns=("shape", "created"),
            show="headings", height=12)
        self.tree.heading("shape", text="shape")
        self.tree.heading("created", text="created")
        self.tree.column("shape", width=60, anchor="center")
        self.tree.column("created", width=160)
        self.tree.grid(row=0, column=0, columnspan=3,
                       padx=4, pady=4, sticky="nsew")

        ttk.Button(tab, text="Histogram",
                   command=self.histogram
                   ).grid(row=1, column=0, sticky="ew", padx=4)
        ttk.Button(tab, text="Refresh",
                   command=self.refresh_runs
                   ).grid(row=1, column=1, sticky="ew", padx=4)

        tab.rowconfigure(0, weight=1)
        tab.columnconfigure((0, 1), weight=1)

        self.refresh_runs()

    def refresh_runs(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for run_id, shape, created in list_runs():
            self.tree.insert("", tk.END, values=(shape, created),
                             iid=str(run_id))

    def _sel_run_id(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Select", "Select a run first")
            return None
        return int(sel[0])

    # ----- History actions -----
    def histogram(self):
        rid = self._sel_run_id()
        if rid is None:
            return
        subprocess.run(["python", ANZ_SCRIPT, "--hist", str(rid)],
                       check=False)
        save_figure(rid, "hist", f"hist_run{rid}.png")
        messagebox.showinfo("Saved", f"hist_run{rid}.png saved")

if __name__ == "__main__":
    SimApp()
