
import numpy as np
from core.simulation import SpermSimulation

def _run(shape):
    c={'shape':shape,'step_length':0.03,'n_simulation':30,'number_of_sperm':1,
       'radius':0.1,'R':0.1,'drop_angle':np.pi/4,'R_spot':0.08,'theta_spot':np.pi/6}
    sim=SpermSimulation(c); sim.simulate()
    diffs=np.linalg.norm(np.diff(sim.traj[0],axis=0),axis=1)
    assert np.allclose(diffs,c['step_length'],atol=1e-6)
    assert np.all(sim.traj[0,:,2]>=-1e-12)  # z>=0

def test_drop_len():
    _run('drop')

def test_spot_len():
    _run('spot')
