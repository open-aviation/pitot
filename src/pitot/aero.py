from typing import Any

from impunity import impunity
from typing_extensions import Annotated

import numpy as np

from . import isa

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


@impunity
def tas2mach(
    tas: Annotated[Any, "kts"], h: Annotated[Any, "ft"]
) -> Annotated[Any, "dimensionless"]:
    """
    :param tas: True Air Speed, (by default in kts)
    :param h: altitude, (by default in ft)

    :return: Mach number (dimensionless)
    """
    a = isa.sound_speed(h)
    M: Annotated[Any, "dimensionless"] = tas / a
    return M


@impunity
def mach2tas(
    M: Annotated[Any, "dimensionless"], h: Annotated[Any, "ft"]
) -> Annotated[Any, "kts"]:
    """
    :param M: Mach number (dimensionless)
    :param h: altitude, (by default in ft)

    :param tas: True Air Speed, (in kts)
    """
    a = isa.sound_speed(h)
    tas: Annotated[Any, "kts"] = M * a
    return tas


@impunity
def eas2tas(
    eas: Annotated[Any, "kts"], h: Annotated[Any, "ft"]
) -> Annotated[Any, "kts"]:
    """
    :param eas: Equivalent Air Speed, (by default in kts)
    :param h: altitude, (by default in ft)

    :return: True Air Speed, (in kts)
    """
    rho = isa.density(h)
    tas: Annotated[Any, "kts"] = eas * np.sqrt(isa.RHO_0 / rho)
    return tas


@impunity
def tas2eas(
    tas: Annotated[Any, "kts"], h: Annotated[Any, "ft"]
) -> Annotated[Any, "kts"]:
    """
    :param tas: True Air Speed, (by default in kts)
    :param h: altitude, (by default in ft)

    :return: Equivalent Air Speed, (in kts)
    """
    rho = isa.density(h)
    eas: Annotated[Any, "kts"] = tas * np.sqrt(rho / isa.RHO_0)
    return eas


@impunity
def cas2tas(
    cas: Annotated[Any, "kts"], h: Annotated[Any, "ft"]
) -> Annotated[Any, "kts"]:
    """
    :param cas: Computed Air Speed, (by default in kts)
    :param h: altitude, (by default in ft)

    :return: True Air Speed, (in kts)
    """
    p, rho, _temp = isa.atmosphere(h)
    qdyn: Annotated[Any, "Pa"] = isa.P_0 * (
        (1.0 + isa.RHO_0 * cas * cas / (7.0 * isa.P_0)) ** 3.5 - 1.0
    )
    tas: Annotated[Any, "m/s"] = np.sqrt(
        7.0 * p / rho * ((1.0 + qdyn / p) ** (2.0 / 7.0) - 1.0)
    )
    tas = np.where(cas < 0, -1 * tas, tas)
    return tas


@impunity
def tas2cas(
    tas: Annotated[Any, "kts"], h: Annotated[Any, "ft"]
) -> Annotated[Any, "kts"]:
    """
    :param tas: True Air Speed, (by default in kts)
    :param h: altitude, (by default in ft)

    :return: Computed Air Speed, (in kts)
    """
    p, rho, _temp = isa.atmosphere(h)
    qdyn = p * ((1.0 + rho * tas * tas / (7.0 * p)) ** 3.5 - 1.0)
    cas: Annotated[Any, "m/s"] = np.sqrt(
        7.0
        * isa.P_0
        / isa.RHO_0
        * ((qdyn / isa.P_0 + 1.0) ** (2.0 / 7.0) - 1.0)
    )
    cas = np.where(tas < 0, -1 * cas, cas)
    return cas


@impunity
def mach2cas(
    M: Annotated[Any, "dimensionless"], h: Annotated[Any, "ft"]
) -> Annotated[Any, "kts"]:
    """
    :param M: Mach number
    :param h: altitude, (by default in ft)

    :return: Computed Air Speed, (in kts)
    """
    tas = mach2tas(M, h)
    cas = tas2cas(tas, h)
    return cas


@impunity
def cas2mach(
    cas: Annotated[Any, "kts"], h: Annotated[Any, "ft"]
) -> Annotated[Any, "dimensionless"]:
    """
    :param cas: Computed Air Speed, (by default in kts)
    :param h: altitude, (by default in ft)

    :return: Mach number (dimensionless)
    """
    tas = cas2tas(cas, h)
    M = tas2mach(tas, h)
    return M
