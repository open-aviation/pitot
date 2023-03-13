from __future__ import annotations

import pytest
from impunity import impunity
from pitot import aero
from typing_extensions import Annotated

import numpy as np
import numpy.typing as npt

# def test_aero() -> None:


@impunity
def test_mach2tas() -> None:
    # https://fr.wikipedia.org/wiki/Nombre_de_Mach
    alt: Annotated[npt.NDArray[np.int64], "m"] = np.array([0, 1000])
    r1 = aero.mach2tas(1, alt)
    r2: Annotated[npt.NDArray[np.float64], "kts"] = np.array([340.3, 336.4])
    assert r1 == pytest.approx(r2, rel=1e-2)


@impunity(rewrite="test_mach2tas_part2.py")
def test_mach2tas_part2() -> None:
    # https://en.wikipedia.org/wiki/Mach_number
    mach: Annotated[npt.NDArray[np.float64], "dimensionless"] = np.array(
        [0.8, 1.2, 5, 10]
    )
    # alt_zero: "m" = 0  # TODO
    alt_zero = 0
    r3 = aero.mach2tas(mach, alt_zero)
    expected_r3: Annotated[npt.NDArray[np.float64], "kts"] = np.array(
        [530, 794, 3308, 6615]
    )
    print(r3)
    print(expected_r3)  # check units
    assert r3 == pytest.approx(expected_r3, rel=1e-2)


# r3 = aero.tas2mach(r2, 0)
# assert r3 == pytest.approx([0.8, 1.2, 5, 10])

# # https://en.wikipedia.org/wiki/Airspeed
# # For example, an aircraft flying at 15,000 feet (4,572 m) in the
# # international standard atmosphere with an IAS of 100 knots (190 km/h), is
# # actually flying at 126 knots (233 km/h) TAS.

# r4 = aero.cas2tas(100, 15_000)
# assert r4 == pytest.approx(126, rel=1e-2)

# r5 = aero.tas2cas(126, 15_000)
# assert r5 == pytest.approx(100, rel=1e-2)

# # https://en.wikipedia.org/wiki/Airspeed
# # With EAS constant, true airspeed increases as aircraft altitude increases.
# # This is because air density decreases with higher altitude.
# r6 = aero.eas2tas(300, [0, 1000, 2000, 5000, 10000])
# assert np.all(r6 >= 300)

# r7 = aero.tas2eas(300, [0, 1000, 2000, 5000, 10000])
# assert np.all(r7 <= 300)

# r8 = aero.mach2cas([0.8, 1.2, 5, 10], 0)
# assert r8 == pytest.approx(
#     aero.tas2cas(aero.mach2tas([0.8, 1.2, 5, 10], 0), 0), rel=1e-2
# )

# r9 = aero.cas2mach(r8, 0)
# assert r9 == pytest.approx([0.8, 1.2, 5, 10], rel=1e-2)
