import pytest

import numpy as np
from pitot import Q_, u
from pitot.convert import temperature


def test_temperature() -> None:
    # value with unit
    r1 = temperature(Q_(0, u.m))
    assert r1.m == pytest.approx(288.15)

    # value without unit
    r2 = temperature(0)
    assert r2.m == pytest.approx(288.15)

    # value array as unit
    altitudes = Q_(np.array([0, 1000, 3000, 9000]), u.ft)
    r3 = temperature(altitudes)
    assert np.allclose(
        r3,
        np.array([288.15, 286.17, 282.21, 270.32]) * u.K,
        rtol=1e-2,
    )

    altitudes_m = 0.3048 * np.array([0, 1000, 3000, 9000])
    r4 = temperature(altitudes_m)
    assert np.allclose(
        r4,
        np.array([288.15, 286.17, 282.21, 270.32]) * u.K,
        rtol=1e-2,
    )
