
from core.simulation import SpermSimulation
import numpy as np
def test_step_length_constant():
    c={'shape':'cube','radius':0.05,'step_length':0.04,'n_simulation':5,'number_of_sperm':1}
    sim=SpermSimulation(c); sim.simulate()
    traj=sim.trajectory[0]
    diffs=np.linalg.norm(np.diff(traj,axis=0),axis=1)
    assert np.allclose(diffs,c['step_length'],atol=1e-6)
