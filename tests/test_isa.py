import numpy as np
import pandas as pd
import pytest

from pitot import Q_, ureg
from pitot.isa import density, pressure, temperature

altitudes = np.array([0, 1000, 3000, 15000, 30000])


def test_temperature() -> None:
    # value with unit
    r1 = temperature(Q_(0, ureg.m))
    assert r1.m == pytest.approx(288.15)

    # value without unit
    r2 = temperature(0)
    assert r2.m == pytest.approx(288.15)

    # value array as unit
    r3 = temperature(Q_(altitudes, ureg.ft))
    assert np.allclose(
        r3,
        np.array([288.15, 286.17, 282.21, 258.43, 228.71]) * ureg.K,
        rtol=1e-2,
    )

    # regular numpy array
    r4 = temperature(0.3048 * altitudes)
    assert np.allclose(
        r4,
        np.array([288.15, 286.17, 282.21, 258.43, 228.71]) * ureg.K,
        rtol=1e-2,
    )

    # pandas Series with unit
    r5 = temperature(pd.Series([0, 1000, 3000, 15000, 30000], dtype="pint[ft]"))
    assert np.allclose(
        r5,
        np.array([288.15, 286.17, 282.21, 258.43, 228.71]) * ureg.K,
        rtol=1e-2,
    )

    # pandas Series without unit
    r6 = temperature(0.3048 * pd.Series(altitudes))
    assert np.allclose(
        r6,
        np.array([288.15, 286.17, 282.21, 258.43, 228.71]) * ureg.K,
        rtol=1e-2,
    )


def test_density() -> None:
    # value with unit
    r1 = density(Q_(0, ureg.m))
    assert r1.m == pytest.approx(1.225)

    # value without unit
    r2 = density(0)
    assert r2.m == pytest.approx(1.225)

    # value array as unit
    r3 = density(Q_(altitudes, ureg.ft))
    assert np.allclose(
        r3,
        np.array([1.2250, 1.1896, 1.1210, 0.7708, 0.4583])
        * ureg.kg
        / ureg.meter**3,
        rtol=1e-2,
    )

    # regular numpy array
    r4 = density(0.3048 * altitudes)
    assert np.allclose(
        r4,
        np.array([1.2250, 1.1896, 1.1210, 0.7708, 0.4583])
        * ureg.kg
        / ureg.meter**3,
        rtol=1e-2,
    )

    # pandas Series with unit
    r5 = density(pd.Series([0, 1000, 3000, 15000, 30000], dtype="pint[ft]"))
    assert np.allclose(
        r5,
        np.array([1.2250, 1.1896, 1.1210, 0.7708, 0.4583])
        * ureg.kg
        / ureg.meter**3,
        rtol=1e-2,
    )

    # pandas Series without unit
    r6 = density(0.3048 * pd.Series(altitudes))
    assert np.allclose(
        r6,
        np.array([1.2250, 1.1896, 1.1210, 0.7708, 0.4583])
        * ureg.kg
        / ureg.meter**3,
        rtol=1e-2,
    )


def test_pressure() -> None:
    # value with unit
    r1 = pressure(Q_(0, ureg.m))
    assert r1.m == pytest.approx(101325)

    # check non-SI equivalent
    assert (r1 - Q_(2116.2, ureg.lbf / ureg.ft**2)).m < 1  # 1 Pa

    # value without unit
    r2 = pressure(0)
    assert r2.m == pytest.approx(101325)

    # value array as unit
    r3 = pressure(Q_(altitudes, ureg.ft))
    assert np.allclose(
        r3,
        np.array([101325, 97717, 90812, 57182, 30090]) * ureg.N / ureg.m**2,
        rtol=1e-2,
    )

    # regular numpy array
    r4 = pressure(0.3048 * altitudes)
    assert np.allclose(
        r4,
        np.array([101325, 97717, 90812, 57182, 30090]) * ureg.N / ureg.m**2,
        rtol=1e-2,
    )

    # pandas Series with unit
    r5 = pressure(pd.Series([0, 1000, 3000, 15000, 30000], dtype="pint[ft]"))
    assert np.allclose(
        r5,
        np.array([101325, 97717, 90812, 57182, 30090]) * ureg.N / ureg.m**2,
        rtol=1e-2,
    )

    # pandas Series without unit
    r6 = pressure(0.3048 * pd.Series(altitudes))
    assert np.allclose(
        r6,
        np.array([101325, 97717, 90812, 57182, 30090]) * ureg.N / ureg.m**2,
        rtol=1e-2,
    )
