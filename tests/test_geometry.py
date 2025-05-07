def test_prepare_random_vec_norm():
    from core.geometry import prepare_new_vector, initial_vec
    c = {'step_length': 0.01, 'deviation': 0.4}
    last = initial_vec(c)
    new  = prepare_new_vector(last, c)
    # ベクトル長が step_length
    import numpy as np
    assert np.isclose(np.linalg.norm(new), 0.01)
import numpy as np
from core.geometry import IO_check_drop, IO_check_spot, IOStatus

def test_IO_check_drop_inside():
    c = {'R': 1.0, 'drop_angle': np.radians(45)}
    p0 = np.zeros(3)
    p1 = np.array([0.0, 0.0, 0.2])
    assert IO_check_drop(p0, p1, c) == IOStatus.INSIDE

def test_IO_check_spot_inside():
    c = {'R_spot': 1.0, 'H_spot': 1.0}
    p0 = np.zeros(3)
    p1 = np.array([0.0, 0.0, 0.5])
    assert IO_check_spot(p0, p1, c) == IOStatus.INSIDE
def test_random_point_inside_drop():
    from core.geometry import random_point_cap, IO_check_drop, IOStatus
    c = {'R': 1.0, 'drop_angle': np.radians(45)}
    p = random_point_cap(c['R'], c['drop_angle'])
    assert IO_check_drop(np.zeros(3), p, c) != IOStatus.OUTSIDE

