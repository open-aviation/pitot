import unittest
from pathlib import Path

from impunity import impunity
from pitot import isa
from typing_extensions import Annotated

import numpy as np
import numpy.typing as npt
import pandas as pd

isa_table = pd.read_fwf(
    Path(__file__).parent / "isa_table.txt", header=[0, 1]
).assign(density=lambda df: isa.RHO_0 * df.density_ratio)

altitude: Annotated[pd.Series, "ft"] = isa_table.altitude.ft


class ISA(unittest.TestCase):
    @impunity
    def test_density(self) -> None:
        expected: Annotated[pd.Series, "kg / m^3"]
        expected = isa_table.density

        result: Annotated[npt.NDArray[np.float64], "kg / m^3"]
        result = isa.density(altitude)

        np.testing.assert_allclose(result, expected, rtol=1e-2)

    @impunity
    def test_pressure(self) -> None:
        expected: Annotated[pd.Series, "hPa"]
        expected = isa_table.pressure.hPa

        result: Annotated[npt.NDArray[np.float64], "hPa"]
        result = isa.pressure(altitude)

        np.testing.assert_allclose(result, expected, rtol=1e-2)

    @impunity
    def test_temperature(self) -> None:
        expected: Annotated[pd.Series, "°C"]
        expected = isa_table.temperature["°C"]

        result: Annotated[npt.NDArray[np.float64], "°C"]
        result = isa.temperature(altitude)

        np.testing.assert_allclose(result, expected, rtol=1e-1)

    @impunity
    def test_soundspeed(self) -> None:
        expected: Annotated[pd.Series, "kts"]
        expected = isa_table.sound_speed.kts

        result: Annotated[npt.NDArray[np.float64], "kts"]
        result = isa.sound_speed(altitude)

        np.testing.assert_allclose(result, expected, rtol=1e-2)
