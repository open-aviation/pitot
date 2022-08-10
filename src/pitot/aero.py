from typing import Any

import numpy as np
import pint

from .isa import P_0, RHO_0, atmosphere, density, sound_speed
from .wrapper import default_units

__all__ = [
    "tas2mach",
    "mach2tas",
    "eas2tas",
    "tas2eas",
    "cas2tas",
    "tas2cas",
    "mach2cas",
    "cas2mach",
]


@default_units(tas="kts", h="ft")
def tas2mach(tas: Any, h: Any) -> pint.Quantity[Any]:
    """
    :param tas: True Air Speed, (by default in kts)
    :param h: altitude, (by default in ft)

    :return: Mach number (dimensionless)
    """
    a = sound_speed(h)
    M = tas / a
    return M.to("dimensionless")  # type: ignore


@default_units(M="dimensionless", h="ft")
def mach2tas(M: Any, h: Any) -> pint.Quantity[Any]:
    """
    :param M: Mach number (dimensionless)
    :param h: altitude, (by default in ft)

    :param tas: True Air Speed, (in kts)
    """
    a = sound_speed(h)
    tas = M * a
    return tas.to("kts")  # type: ignore


@default_units(eas="kts", h="ft")
def eas2tas(eas: Any, h: Any) -> pint.Quantity[Any]:
    """
    :param eas: Equivalent Air Speed, (by default in kts)
    :param h: altitude, (by default in ft)

    :return: True Air Speed, (in kts)
    """
    rho = density(h)
    tas = eas * np.sqrt(RHO_0 / rho)
    return tas.to("kts")  # type: ignore


@default_units(tas="kts", h="ft")
def tas2eas(tas: Any, h: Any) -> pint.Quantity[Any]:
    """
    :param tas: True Air Speed, (by default in kts)
    :param h: altitude, (by default in ft)

    :return: Equivalent Air Speed, (in kts)
    """
    rho = density(h)
    eas = tas * np.sqrt(rho / RHO_0)
    return eas.to("kts")  # type: ignore


@default_units(cas="kts", h="ft")
def cas2tas(cas: Any, h: Any) -> pint.Quantity[Any]:
    """
    :param cas: Computed Air Speed, (by default in kts)
    :param h: altitude, (by default in ft)

    :return: True Air Speed, (in kts)
    """
    p, rho, _temp = atmosphere(h)
    qdyn = P_0 * ((1.0 + RHO_0 * cas * cas / (7.0 * P_0)) ** 3.5 - 1.0)
    tas = np.sqrt(7.0 * p / rho * ((1.0 + qdyn / p) ** (2.0 / 7.0) - 1.0))
    tas = np.where(cas < 0, -1 * tas, tas)
    return tas.to("kts")  # type: ignore


@default_units(tas="kts", h="ft")
def tas2cas(tas: Any, h: Any) -> pint.Quantity[Any]:
    """
    :param tas: True Air Speed, (by default in kts)
    :param h: altitude, (by default in ft)

    :return: Computed Air Speed, (in kts)
    """
    p, rho, _temp = atmosphere(h)
    qdyn = p * ((1.0 + rho * tas * tas / (7.0 * p)) ** 3.5 - 1.0)
    cas = np.sqrt(7.0 * P_0 / RHO_0 * ((qdyn / P_0 + 1.0) ** (2.0 / 7.0) - 1.0))
    cas = np.where(tas < 0, -1 * cas, cas)
    return cas.to("kts")  # type: ignore


@default_units(M="dimensionless", h="ft")
def mach2cas(M: Any, h: Any) -> pint.Quantity[Any]:
    """
    :param M: Mach number
    :param h: altitude, (by default in ft)

    :return: Computed Air Speed, (in kts)
    """
    tas = mach2tas(M, h)
    cas = tas2cas(tas, h)
    return cas.to("kts")


@default_units(cas="kts", h="ft")
def cas2mach(cas: Any, h: Any) -> pint.Quantity[Any]:
    """
    :param cas: Computed Air Speed, (by default in kts)
    :param h: altitude, (by default in ft)

    :return: Mach number (dimensionless)
    """
    tas = cas2tas(cas, h)
    M = tas2mach(tas, h)
    return M.to("dimensionless")
