import pytest

import numpy as np
from pitot import Q_, u
from pitot.isa import temperature, density, pressure


def test_temperature() -> None:
    # value with unit
    r1 = temperature(Q_(0, u.m))
    assert r1.m == pytest.approx(288.15)

    # value without unit
    r2 = temperature(0)
    assert r2.m == pytest.approx(288.15)

    # value array as unit
    altitudes = Q_(np.array([0, 1000, 3000, 15000, 30000]), u.ft)
    r3 = temperature(altitudes)
    assert np.allclose(
        r3,
        np.array([288.15, 286.17, 282.21, 258.43, 228.71]) * u.K,
        rtol=1e-2,
    )

    altitudes_m = 0.3048 * np.array([0, 1000, 3000, 15000, 30000])
    r4 = temperature(altitudes_m)
    assert np.allclose(
        r4,
        np.array([288.15, 286.17, 282.21, 258.43, 228.71]) * u.K,
        rtol=1e-2,
    )


def test_density() -> None:
    # value with unit
    r1 = density(Q_(0, u.m))
    assert r1.m == pytest.approx(1.225)

    # value without unit
    r2 = density(0)
    assert r2.m == pytest.approx(1.225)

    # value array as unit
    altitudes = Q_(np.array([0, 1000, 3000, 15000, 30000]), u.ft)
    r3 = density(altitudes)
    assert np.allclose(
        r3,
        np.array([1.2250, 1.1896, 1.1210, 0.7708, 0.4583])
        * u.kg
        / u.meter ** 3,
        rtol=1e-2,
    )

    altitudes_m = 0.3048 * np.array([0, 1000, 3000, 15000, 30000])
    r4 = density(altitudes_m)
    assert np.allclose(
        r4,
        np.array([1.2250, 1.1896, 1.1210, 0.7708, 0.4583])
        * u.kg
        / u.meter ** 3,
        rtol=1e-2,
    )


def test_pressure() -> None:
    # value with unit
    r1 = pressure(Q_(0, u.m))
    assert r1.m == pytest.approx(101325)

    # check non-SI equivalent
    assert (r1 - Q_(2116.2, u.lbf / u.ft ** 2)).m < 1  # 1 Pa

    # value without unit
    r2 = pressure(0)
    assert r2.m == pytest.approx(101325)

    # value array as unit
    altitudes = Q_(np.array([0, 1000, 3000, 15000, 30000]), u.ft)
    r3 = pressure(altitudes)
    assert np.allclose(
        r3,
        np.array([101325, 97717, 90812, 57182, 30090]) * u.N / u.m ** 2,
        rtol=1e-2,
    )

    altitudes_m = 0.3048 * np.array([0, 1000, 3000, 15000, 30000])
    r4 = pressure(altitudes_m)
    assert np.allclose(
        r4,
        np.array([101325, 97717, 90812, 57182, 30090]) * u.N / u.m ** 2,
        rtol=1e-2,
    )
