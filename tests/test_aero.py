from __future__ import annotations

import unittest

from impunity import impunity
from pitot import aero
from pitot import isa
from typing_extensions import Annotated

import numpy as np
import numpy.typing as npt


class Aero(unittest.TestCase):
    @impunity
    def test_mach2tas(self) -> None:
        raised = False
        try:
            alt: Annotated[npt.NDArray[np.int64], "m"] = np.array([0, 1000])
            r1: Annotated[npt.NDArray[np.float64], "m/s"] = aero.mach2tas(
                1, alt
            )
            r2: Annotated[npt.NDArray[np.float64], "m/s"] = np.array(
                [340.3, 336.4]
            )
            np.testing.assert_allclose(r1, r2, rtol=1e-2)
        except AssertionError:
            raised = True

        self.assertFalse(raised)

    @impunity
    def test_mach2tas_part2(self) -> None:
        raised = False
        try:
            # https://en.wikipedia.org/wiki/Mach_number
            mach: Annotated[
                npt.NDArray[np.float64], "dimensionless"
            ] = np.array([0.8, 1.2, 5, 10])
            r3 = aero.mach2tas(mach, isa.SEA_ALT)
            expected_r3: Annotated[npt.NDArray[np.float64], "kts"] = np.array(
                [530, 794, 3308, 6615]
            )

            np.testing.assert_allclose(r3, expected_r3, rtol=1e-2)
        except AssertionError:
            raised = True

        self.assertFalse(raised)

    @impunity
    def test_tas2mach(self) -> None:
        raised = False
        try:
            r3: Annotated[npt.NDArray[np.float64], "kts"] = np.array(
                [530, 794, 3308, 6615]
            )
            r4 = aero.tas2mach(r3, 0)
            expected_r4: Annotated[npt.NDArray[np.float64], "kts"] = np.array(
                [0.8, 1.2, 5, 10]
            )

            np.testing.assert_allclose(r4, expected_r4, rtol=1e-2)
        except AssertionError:
            raised = True

        self.assertFalse(raised)

    @impunity
    def test_cas2tas(self) -> None:
        # https://en.wikipedia.org/wiki/Airspeed
        # For example, an aircraft flying at 15,000 feet (4,572 m) in the
        # international standard atmosphere with an IAS of 100 knots
        # (190 km/h), is actually flying at 126 knots (233 km/h) TAS.

        r4 = aero.cas2tas(100, 15_000)
        self.assertAlmostEqual(r4, 125.790, places=1)

    @impunity
    def test_cas2tas_part2(self) -> None:
        r5 = aero.tas2cas(126, 15_000)
        self.assertAlmostEqual(r5, 100.167, delta=1e-2)

    @impunity
    def test_cas2tas_part3(self) -> None:
        r6 = aero.eas2tas(300, np.array([0, 1000, 2000, 5000, 10000]))
        assert np.all(r6 >= 300)

    @impunity
    def test_cas2tas_part4(self) -> None:
        r7 = aero.tas2eas(300, np.array([0, 1000, 2000, 5000, 10000]))
        assert np.all(r7 <= 300)

    @impunity
    def test_cas2tas_part5(self) -> None:
        raised = False
        try:
            r8 = aero.mach2cas(np.array([0.8, 1.2, 5, 10]), 0)
            r8_expected = aero.mach2tas(np.array([0.8, 1.2, 5, 10]), 0)
            r8_expected = aero.tas2cas(r8_expected, 0)
            np.testing.assert_allclose(r8, r8_expected, rtol=1e-2)
        except AssertionError:
            raised = True

        self.assertFalse(raised)

    @impunity
    def test_cas2tas_part6(self) -> None:
        raised = False
        try:
            r8 = aero.mach2cas(np.array([0.8, 1.2, 5, 10]), 0)
            r9 = aero.cas2mach(r8, 0)
            np.testing.assert_allclose(
                r9, np.array([0.8, 1.2, 5, 10]), rtol=1e-2
            )
        except AssertionError:
            raised = True

        self.assertFalse(raised)


if __name__ == "__main__":
    unittest.main()
