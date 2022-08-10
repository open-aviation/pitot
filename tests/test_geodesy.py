import numpy as np
import pytest

from pitot import Q_
from pitot.geodesy import bearing, destination, distance, greatcircle


def test_geodesy() -> None:

    # nautical mile definition
    assert distance(0, 0, 0, 1 / 60).to("nmi").m == pytest.approx(1, rel=1e-2)

    # pointing to the East
    assert bearing(0, 0, 0, 45) == 90.0

    # running along Greenwich meridian: longitude remains 0
    assert destination(0, 0, 0, 123456)[1] == 0

    # nautical mile definition
    assert destination(0, 0, 90, Q_(60, "nmi")) == pytest.approx(
        (0, 1, -90), rel=1e-2
    )

    x = np.stack(greatcircle(0, 0, 0, 45, 44))
    assert sum(x[:, 0]) == 0
    assert sum(x[:, 1]) == 45 * 22

    # Vector version
    d = distance(x[1:, 0], x[1:, 1], x[:-1, 0], x[:-1, 1])
    assert d.max().m == pytest.approx(d.min().m)

    b = bearing(x[:-1, 0], x[:-1, 1], x[1:, 0], x[1:, 1])
    assert b.max() == pytest.approx(b.min())
