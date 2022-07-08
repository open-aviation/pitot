import pytest

from pitot.convert import u, temperature
import numpy as np


def test_temperature() -> None:
    assert temperature(0 * u.m).m == pytest.approx(288.15)

    # assert temperature(0) == pytest.approx(288.15)

    altitudes = np.array([0, 1000, 3000, 9000]) * u.ft
    assert np.allclose(
        temperature(altitudes),
        np.array([288.15, 286.17, 282.21, 270.32]) * u.K,
        rtol=1e-2,
    )

    # assert temperature([0, 1000, 3000, 9000]) == [
    #     288.15,
    #     286.17,
    #     282.21,
    #     270.32,
    # ]
