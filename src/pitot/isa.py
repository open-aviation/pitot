import logging
from typing import Any

import numpy as np
import pint

from . import Q_, ureg
from .wrapper import default_units

__all__ = ["temperature", "density", "pressure", "sound_speed"]

_log = logging.getLogger(__name__)


GAMMA = 1.40  # Cp/Cv for a
R = Q_(287.05287, "m^2 / (s^2 * K)")  # gas constant, sea level ISA
RHO_0 = Q_(1.225, "kg / m^3")
SPECIFIC_GAS_CONSTANT = Q_(287.05287, "J/kg/K")
STRATOSPHERE_TEMP = Q_(216.65, ureg.K)  # until altitude = 22km


@default_units(h=ureg.meter)
def temperature(h: Any) -> pint.Quantity[Any]:
    """Temperature of ISA atmosphere

    :param h: the altitude (by default in meters), :math:`0 < h < 84852`
        (will be clipped when outside range, integer input allowed)

    :return: the temperature (in K)

    """
    temp = np.maximum(
        Q_(288.15, "K") - Q_(0.0065, "K/m") * h,
        STRATOSPHERE_TEMP,
    )
    return temp  # type: ignore


@default_units(h=ureg.meter)
def density(h: Any) -> pint.Quantity[Any]:
    """Density of ISA atmosphere

    :param h: the altitude (by default in meters), :math:`0 < h < 84852`
        (will be clipped when outside range, integer input allowed)

    :return: the density :math:`\\rho`, in kg/m3

    """
    temp = temperature(h)
    density_troposphere = RHO_0 * (temp / Q_(288.15, ureg.K)) ** 4.256848
    delta = np.maximum(Q_(0, ureg.meter), h - Q_(11000, ureg.meter))
    density: pint.Quantity[Any] = density_troposphere * np.exp(
        -delta / Q_(6341.5522, ureg.meter)
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
def sound_speed(h: Any) -> pint.Quantity[Any]:
    """Speed of sound in ISA atmosphere

    :param h: the altitude (by default in meters), :math:`0 < h < 84852`
        (will be clipped when outside range, integer input allowed)

    :return: the speed of sound :math:`a`, in m/s

    """
    temp = temperature(h)
    a = np.sqrt(GAMMA * R * temp)
    return a  # type: ignore
