
import numpy as np
from core.simulation import SpermSimulation

def test_multiple_sperm_shape():
    c = {
        'shape':'cube',
        'radius':1.0,
        'n_simulation':50,
        'number_of_sperm':10,
        'step_length':0.01,
        'R':1.0,
        'drop_angle':np.pi/4,
        'R_spot':0.1,
        'theta_spot':np.pi/6
    }
    sim = SpermSimulation(c)
    sim.simulate()
    assert sim.trajectory.shape == (10, 50, 3)
