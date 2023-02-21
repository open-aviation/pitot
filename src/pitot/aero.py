from typing import Any

import numpy as np
from impunity import impunity  # type: ignore
from typing_extensions import Annotated

from . import isa

# from .isa import P_0, RHO_0, atmosphere, density, sound_speed

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


@impunity  # type: ignore
def tas2mach(
    tas: Annotated[Any, "kts"], h: Annotated[Any, "ft"]
) -> Annotated[Any, "dimensionless"]:
    """
    :param tas: True Air Speed, (by default in kts)
    :param h: altitude, (by default in ft)

    :return: Mach number (dimensionless)
    """
    a: Annotated[Any, "m/s"] = isa.sound_speed(h)
    M: Annotated[Any, "dimensionless"] = tas / a
    return M


@impunity  # type: ignore
def mach2tas(
    M: Annotated[Any, "dimensionless"], h: Annotated[Any, "ft"]
) -> Annotated[Any, "kts"]:
    """
    :param M: Mach number (dimensionless)
    :param h: altitude, (by default in ft)

    :param tas: True Air Speed, (in kts)
    """
    a: Annotated[Any, "m/s"] = isa.sound_speed(h)
    tas: Annotated[Any, "kts"] = M * a
    return tas


@impunity  # type: ignore
def eas2tas(
    eas: Annotated[Any, "kts"], h: Annotated[Any, "ft"]
) -> Annotated[Any, "kts"]:
    """
    :param eas: Equivalent Air Speed, (by default in kts)
    :param h: altitude, (by default in ft)

    :return: True Air Speed, (in kts)
    """
    rho: Annotated[Any, "kg * m^-3"] = isa.density(h)
    tas: Annotated[Any, "kts"] = eas * np.sqrt(isa.RHO_0 / rho)
    return tas


@impunity  # type: ignore
def tas2eas(
    tas: Annotated[Any, "kts"], h: Annotated[Any, "ft"]
) -> Annotated[Any, "kts"]:
    """
    :param tas: True Air Speed, (by default in kts)
    :param h: altitude, (by default in ft)

    :return: Equivalent Air Speed, (in kts)
    """
    rho: Annotated[Any, "kg * m^-3"] = isa.density(h)
    eas: Annotated[Any, "kts"] = tas * np.sqrt(rho / isa.RHO_0)
    return eas


@impunity  # type: ignore
def cas2tas(
    cas: Annotated[Any, "kts"], h: Annotated[Any, "ft"]
) -> Annotated[Any, "kts"]:
    """
    :param cas: Computed Air Speed, (by default in kts)
    :param h: altitude, (by default in ft)

    :return: True Air Speed, (in kts)
    """
    p, rho, _temp = isa.atmosphere(h)
    qdyn = isa.P_0 * (
        (1.0 + isa.RHO_0 * cas * cas / (7.0 * isa.P_0)) ** 3.5 - 1.0
    )
    tas: Annotated[Any, "kts"] = np.sqrt(
        7.0 * p / rho * ((1.0 + qdyn / p) ** (2.0 / 7.0) - 1.0)
    )
    tas = np.where(cas < 0, -1 * tas, tas)
    return tas


@impunity  # type: ignore
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
    cas: Annotated[Any, "kts"] = np.sqrt(
        7.0
        * isa.P_0
        / isa.RHO_0
        * ((qdyn / isa.P_0 + 1.0) ** (2.0 / 7.0) - 1.0)
    )
    cas = np.where(tas < 0, -1 * cas, cas)
    return cas


@impunity  # type: ignore
def mach2cas(
    M: Annotated[Any, "dimensionless"], h: Annotated[Any, "ft"]
) -> Annotated[Any, "kts"]:
    """
    :param M: Mach number
    :param h: altitude, (by default in ft)

    :return: Computed Air Speed, (in kts)
    """
    tas: Annotated[Any, "kts"] = mach2tas(M, h)
    cas: Annotated[Any, "kts"] = tas2cas(tas, h)
    return cas


@impunity  # type: ignore
def cas2mach(
    cas: Annotated[Any, "kts"], h: Annotated[Any, "ft"]
) -> Annotated[Any, "dimensionless"]:
    """
    :param cas: Computed Air Speed, (by default in kts)
    :param h: altitude, (by default in ft)

    :return: Mach number (dimensionless)
    """
    tas = cas2tas(cas, h)
    M: Annotated[Any, "dimensionless"] = tas2mach(tas, h)
    return M
