from __future__ import annotations

import unittest

from impunity import impunity
from pitot import aero, isa
from typing_extensions import Annotated

import numpy as np
import numpy.typing as npt


class Aero(unittest.TestCase):
    @impunity
    def test_mach2tas(self) -> None:
        raised = False
        try:
            altitude: Annotated[npt.NDArray[np.int64], "m"]
            altitude = np.array([0, 1000])

            result: Annotated[npt.NDArray[np.float64], "m/s"]
            result = aero.mach2tas(1, altitude)

            expected: Annotated[npt.NDArray[np.float64], "m/s"]
            expected = np.array([340.3, 336.4])

            np.testing.assert_allclose(result, expected, rtol=1e-2)
        except AssertionError:
            raised = True

        self.assertFalse(raised)

    @impunity
    def test_mach2tas_part2(self) -> None:
        raised = False
        try:
            # https://en.wikipedia.org/wiki/Mach_number
            mach: Annotated[npt.NDArray[np.float64], "dimensionless"]
            mach = np.array([0.8, 1.2, 5, 10])

            result = aero.mach2tas(mach, isa.SEA_ALT)

            expected: Annotated[npt.NDArray[np.float64], "kts"]
            expected = np.array([530, 794, 3308, 6615])

            np.testing.assert_allclose(result, expected, rtol=1e-2)
        except AssertionError:
            raised = True

        self.assertFalse(raised)

    @impunity
    def test_tas2mach(self) -> None:
        raised = False
        try:
            speed: Annotated[npt.NDArray[np.float64], "kts"]
            speed = np.array([530, 794, 3308, 6615])

            result = aero.tas2mach(speed, 0)

            expected: Annotated[npt.NDArray[np.float64], "kts"]
            expected = np.array([0.8, 1.2, 5, 10])

            np.testing.assert_allclose(result, expected, rtol=1e-2)
        except AssertionError:
            raised = True

        self.assertFalse(raised)

    @impunity
    def test_cas2tas(self) -> None:
        # https://en.wikipedia.org/wiki/Airspeed
        # For example, an aircraft flying at 15,000 feet (4,572 m) in the
        # international standard atmosphere with an IAS of 100 knots
        # (190 km/h), is actually flying at 126 knots (233 km/h) TAS.

        result = aero.cas2tas(100, 15_000)
        self.assertAlmostEqual(result, 125.790, places=1)

    @impunity
    def test_cas2tas_part2(self) -> None:
        result = aero.tas2cas(126, 15_000)
        self.assertAlmostEqual(result, 100.167, delta=1e-2)

    @impunity
    def test_cas2tas_part3(self) -> None:
        result = aero.eas2tas(300, np.array([0, 1000, 2000, 5000, 10000]))
        assert np.all(result >= 300)

    @impunity
    def test_cas2tas_part4(self) -> None:
        result = aero.tas2eas(300, np.array([0, 1000, 2000, 5000, 10000]))
        assert np.all(result <= 300)

    @impunity
    def test_cas2tas_part5(self) -> None:
        raised = False
        try:
            result = aero.mach2cas(np.array([0.8, 1.2, 5, 10]), 0)
            expected = aero.mach2tas(np.array([0.8, 1.2, 5, 10]), 0)
            expected = aero.tas2cas(expected, 0)
            np.testing.assert_allclose(result, expected, rtol=1e-2)
        except AssertionError:
            raised = True

        self.assertFalse(raised)

    @impunity
    def test_cas2tas_part6(self) -> None:
        raised = False
        try:
            mach = np.array([0.8, 1.2, 5, 10])

            cas = aero.mach2cas(mach, 0)
            result = aero.cas2mach(cas, 0)

            np.testing.assert_allclose(result, mach, rtol=1e-2)
        except AssertionError:
            raised = True

        self.assertFalse(raised)


if __name__ == "__main__":
    unittest.main()
