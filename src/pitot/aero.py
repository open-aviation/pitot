from typing import Any

import isa
from impunity import impunity
from typing_extensions import Annotated

import numpy as np

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

    a = isa.sound_speed(h)
    M = cas2mach(cas, h)
    tas = a * M
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

    M = tas2mach(tas, h)
    cas: Annotated[Any, "kts"] = mach2cas(M, h)
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

    p, _, _ = isa.atmosphere(h)
    a_0 = isa.sound_speed(isa.SEA_ALT)
    qdyn = p * ((1.0 + M**2 / 5.0) ** 3.5 - 1.0)
    cas: Annotated[Any, "kts"] = a_0 * np.sqrt(
        5.0 * ((1.0 + qdyn / isa.P_0) ** (2.0 / 7.0) - 1.0)
    )

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

    p, _, _ = isa.atmosphere(h)
    a_0 = isa.sound_speed(isa.SEA_ALT)
    qdyn = isa.P_0 * ((1.0 + (cas / a_0) ** 2 / 5.0) ** 3.5 - 1.0)
    M: Annotated[Any, "kts"] = np.sqrt(
        5.0 * ((1.0 + qdyn / p) ** (2.0 / 7.0) - 1.0)
    )

    return M
