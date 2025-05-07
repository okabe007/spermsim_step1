import numpy as np
from reflection.runner import run_all
from core.geometry import IO_check_cube, IO_check_drop, IO_check_spot, IOStatus

TOL = 1e-6
ALLOW = (IOStatus.INSIDE, IOStatus.TEMP_SURFACE, IOStatus.OUTSIDE)

def _chk(sim, step):
    d = np.linalg.norm(np.diff(sim.trajectory[0], axis=0), axis=1)
    # drop_zm は 1step 目が 0 になるので 2step 目以降を確認
    assert np.allclose(d[1:], step, atol=TOL)

def test_cube_reflection():
    c = {'shape':'cube','radius':0.1,'step_length':0.02,'n_simulation':5}
    sims = list(run_all('cube', c));  assert len(sims) == 18
    for _, s in sims:
        _chk(s, c['step_length'])
        st = IO_check_cube(s.trajectory[0,0], s.trajectory[0,1], {'radius': c['radius']})
        assert st in ALLOW

def test_drop_reflection():
    c = {'shape':'drop','R':0.1,'drop_angle':0.52,'step_length':0.02,'n_simulation':5}
    sims = list(run_all('drop', c));  assert len(sims) == 6
    for _, s in sims:
        _chk(s, c['step_length'])
        st = IO_check_drop(s.trajectory[0,0], s.trajectory[0,1], c)
        assert st in ALLOW

def test_spot_reflection():
    c = {'shape':'spot','R_spot':0.1,'theta_spot':0.52,'step_length':0.02,'n_simulation':5}
    sims = list(run_all('spot', c));  assert len(sims) == 10
    for _, s in sims:
        _chk(s, c['step_length'])
        st = IO_check_spot(s.trajectory[0,0], s.trajectory[0,1], c)
        assert st in ALLOW
