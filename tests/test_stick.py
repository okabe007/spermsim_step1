
import numpy as np
from core.simulation import SpermSimulation

def test_step_length_constant():
    c = {'shape':'cube','radius':0.05,'step_length':0.02,'n_simulation':20,'number_of_sperm':1}
    sim = SpermSimulation(c)
    sim.simulate()
    diffs = np.linalg.norm(np.diff(sim.trajectory[0], axis=0), axis=1)
    assert np.allclose(diffs, c['step_length'], atol=1e-6)
