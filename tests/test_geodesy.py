import unittest
from typing import Any

from impunity import impunity
from typing_extensions import Annotated

import numpy as np
from pitot.geodesy import bearing, destination, distance, greatcircle

zero: Annotated[int, "dimensionless"] = 0
boop: Annotated[int, "dimensionless"] = 0
value_1: Annotated[float, "dimensionless"] = 1 / 60
value_2: Annotated[float, "dimensionless"] = 45
value_3: Annotated[float, "dimensionless"] = 123456
nmi = Annotated[Any, "nmi"]
m = Annotated[Any, "m"]


class Geodesy(unittest.TestCase):
    @impunity
    def test_nautical_miles(self) -> None:
        dist_nautical: Annotated[Any, "nmi"] = 1
        dist_meters: Annotated[Any, "m"] = dist_nautical
        self.assertAlmostEqual(
            dist_meters,
            distance(zero, zero, lat2=zero, lon2=value_1),
            delta=5,
        )

    @impunity
    def test_equator_bearing(self) -> None:
        # pointing to the East
        self.assertEqual(bearing(zero, zero, lon2=value_2, lat2=zero), 90.0)

    @impunity
    def test_equator_destination(self) -> None:
        # running along Greenwich meridian: longitude remains 0
        self.assertEqual(destination(zero, zero, zero, value_3)[1], 0)

    @impunity
    def test_destination_equator(self) -> None:
        # running along Greenwich meridian: longitude remains 0
        distance: Annotated[Any, "nmi"] = 60
        res1, res2, res3 = destination(0, 0, 90, distance)
        self.assertEqual(res1, 0)
        self.assertAlmostEqual(res2, 1, delta=1e-2)
        self.assertEqual(res3, -90)

    @impunity
    def test_greatcircle(self) -> None:
        x = np.stack(greatcircle(0, 0, 0, 45, 44))
        assert sum(x[:, 0]) == 0
        assert sum(x[:, 1]) == 45 * 22

    @impunity
    def test_greatcircle_distance(self) -> None:
        x = np.stack(greatcircle(0, 0, 0, 45, 44))

        # Vector version
        d = distance(x[1:, 0], x[1:, 1], x[:-1, 0], x[:-1, 1])
        self.assertAlmostEqual(d.max(), d.min())

    @impunity
    def test_greatcircle_bearing(self) -> None:
        x = np.stack(greatcircle(0, 0, 0, 45, 44))

        b = bearing(x[:-1, 0], x[:-1, 1], x[1:, 0], x[1:, 1])
        self.assertAlmostEqual(b.max(), b.min())


if __name__ == "__main__":
    unittest.main()
