from typing import Any, Tuple

import numpy as np
import pint

from . import Q_, ureg
from .wrapper import default_units

__all__ = ["temperature", "density", "pressure", "sound_speed"]


GAMMA = Q_(1.40, "dimensionless")  # Cp/Cv for air
P_0 = Q_(101325.0, "Pa")  # sea level pressure ISA
R = Q_(287.05287, "m^2 / (s^2 * K)")  # gas constant, sea level ISA
RHO_0 = Q_(1.225, "kg / m^3")  # sea level density ISA
SPECIFIC_GAS_CONSTANT = Q_(287.05287, "J/kg/K")
STRATOSPHERE_TEMP = Q_(216.65, "K")  # until altitude = 22km


@default_units(h=ureg.meter)
def temperature(h: Any) -> pint.Quantity[Any]:
    """Temperature of ISA atmosphere

    :param h: the altitude (by default in meters), :math:`0 < h < 84852`
        (will be clipped when outside range, integer input allowed)

    :return: the temperature (in K)

    """
    temp: pint.Quantity[Any] = np.maximum(  # type: ignore
        Q_(288.15, "K") - Q_(0.0065, "K/m") * h,
        STRATOSPHERE_TEMP,
    )
    return temp


@default_units(h=ureg.meter)
def density(h: Any) -> pint.Quantity[Any]:
    """Density of ISA atmosphere

    :param h: the altitude (by default in meters), :math:`0 < h < 84852`
        (will be clipped when outside range, integer input allowed)

    :return: the density :math:`\\rho`, in kg/m3

    """
    temp = temperature(h)
    density_troposphere = RHO_0 * (temp / Q_(288.15, "K")) ** 4.256848
    delta = np.maximum(Q_(0, "m"), h - Q_(11000, "m"))
    density: pint.Quantity[Any] = density_troposphere * np.exp(
        -delta / Q_(6341.5522, "m")
    )
    return density


@default_units(h=ureg.meter)
def pressure(h: Any) -> pint.Quantity[Any]:
    """Pressure of ISA atmosphere

    :param h: the altitude (by default in meters), :math:`0 < h < 84852`
        (will be clipped when outside range, integer input allowed)

    :return: the pressure, in Pa

    """
    temp = temperature(h)
    den = density(h)
    press: pint.Quantity[Any] = den * temp * SPECIFIC_GAS_CONSTANT
    return press


@default_units(h=ureg.meter)
def atmosphere(
    h: Any,
) -> Tuple[pint.Quantity[Any], pint.Quantity[Any], pint.Quantity[Any]]:
    """Pressure of ISA atmosphere

    :param h: the altitude (by default in meters), :math:`0 < h < 84852`
        (will be clipped when outside range, integer input allowed)

    :return: a tuple (pressure, density, temperature)

    """
    temp: pint.Quantity[Any] = np.maximum(  # type: ignore
        Q_(288.15, "K") - Q_(0.0065, "K/m") * h,
        STRATOSPHERE_TEMP,
    )
    density_troposphere = RHO_0 * (temp / Q_(288.15, "K")) ** 4.256848
    delta = np.maximum(Q_(0, "m"), h - Q_(11000, "m"))
    den: pint.Quantity[Any] = density_troposphere * np.exp(
        -delta / Q_(6341.5522, "m")
    )
    press: pint.Quantity[Any] = den * temp * SPECIFIC_GAS_CONSTANT
    return press, den, temp


@default_units(h=ureg.meter)
def sound_speed(h: Any) -> pint.Quantity[Any]:
    """Speed of sound in ISA atmosphere

    :param h: the altitude (by default in meters), :math:`0 < h < 84852`
        (will be clipped when outside range, integer input allowed)

    :return: the speed of sound :math:`a`, in m/s

    """
    temp = temperature(h)
    a = np.sqrt(GAMMA * R * temp)
    return a  # type: ignore
