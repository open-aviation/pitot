from typing import Any

import numpy as np
import pytest
from impunity import impunity
from typing_extensions import Annotated

from pitot.geodesy import bearing, destination, distance, greatcircle

zero: Annotated[int, "dimensionless"] = 0
boop: Annotated[int, "dimensionless"] = 0
value_1: Annotated[float, "dimensionless"] = 1 / 60
value_2: Annotated[float, "dimensionless"] = 45
value_3: Annotated[float, "dimensionless"] = 123456
nmi = Annotated[Any, "nmi"]
m = Annotated[Any, "m"]


@impunity
def test_nautical_miles() -> None:
    dist_nautical: Annotated[Any, "nmi"] = 1
    dist_meters: Annotated[Any, "m"] = dist_nautical
    assert (
        pytest.approx(
            distance(zero, zero, lat2=zero, lon2=value_1),
            rel=1e-2,
        )
        == dist_meters
    )


@impunity
def test_equator_bearing() -> None:
    # pointing to the East
    assert bearing(zero, zero, lon2=value_2, lat2=zero) == 90.0


@impunity
def test_equator_destination() -> None:
    # running along Greenwich meridian: longitude remains 0
    assert destination(zero, zero, zero, value_3)[1] == 0


@impunity
def test_destination_equator() -> None:
    # running along Greenwich meridian: longitude remains 0
    distance: Annotated[Any, "nmi"] = 60
    res = destination(0, 0, 90, distance)
    assert res == pytest.approx((0, 1, -90), rel=1e-2)


@impunity
def test_destination_nmi() -> None:
    distance: Annotated[Any, "nmi"] = 60
    assert destination(0, 0, 90, distance) == pytest.approx(
        (0, 1, -90), rel=1e-2
    )


@impunity
def test_greatcircle() -> None:
    x = np.stack(greatcircle(0, 0, 0, 45, 44))
    assert sum(x[:, 0]) == 0
    assert sum(x[:, 1]) == 45 * 22


@impunity
def test_greatcircle_distance() -> None:
    x = np.stack(greatcircle(0, 0, 0, 45, 44))

    # Vector version
    d = distance(x[1:, 0], x[1:, 1], x[:-1, 0], x[:-1, 1])
    assert d.max() == pytest.approx(d.min())


@impunity
def test_greatcircle_bearing() -> None:
    x = np.stack(greatcircle(0, 0, 0, 45, 44))

    b = bearing(x[:-1, 0], x[:-1, 1], x[1:, 0], x[1:, 1])
    assert b.max() == pytest.approx(b.min())
