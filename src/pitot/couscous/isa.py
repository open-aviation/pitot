from typing import Any, Tuple

import numpy as np
import pint

from .. import Q_, ureg
from ..wrapper import default_units
from ..wrapper import couscous

__all__ = ["temperature", "density", "pressure", "sound_speed"]

Pa = s = m = kg = K = J = Any

GAMMA = 1.40  # Cp/Cv for air
P_0: "Pa" = 101325.0  # sea level pressure ISA
R: "m^2 / (s^2 * K)" = 287.05287  # gas constant, sea level ISA
RHO_0: "kg / m^3" = 1.225  # sea level density ISA
SPECIFIC_GAS_CONSTANT: "J/kg/K" = 287.05287
STRATOSPHERE_TEMP: "K" = 216.65  # until altitude = 22km
G_0: "m / s^2" = 9.80665  # Gravitational acceleration
BETA_T: "K / m" = -0.0065  # Temperature gradient below tropopause, ISA
TROPOPAUSE_PRESS: "Pa" = 22632.0401  # pressure at tropopause, ISA
H_TROP: "m" = 11000  # tropopause altitude


def temperature(h: "m") -> "K":
    """Temperature of ISA atmosphere

    :param h: the altitude (by default in meters), :math:`0 < h < 84852`
        (will be clipped when outside range, integer input allowed)

    :return: the temperature (in K)

    """

    temp_0: "K" = 288.15
    c: "K/m" = 0.0065
    temp: "K" = np.maximum(
        temp_0 - c * h,
        STRATOSPHERE_TEMP,
    )
    return temp


def density(h: "m") -> "Pa":
    """Density of ISA atmosphere

    :param h: the altitude (by default in meters), :math:`0 < h < 84852`
        (will be clipped when outside range, integer input allowed)

    :return: the density :math:`\\rho`, in kg/m3

    """
    temp: "K" = temperature(h)
    density_troposphere = RHO_0 * (temp / Q_(288.15, "K")) ** 4.256848
    delta = np.maximum(Q_(0, "m"), h - Q_(11000, "m"))
    density: "Pa" = density_troposphere * np.exp(-delta / Q_(6341.5522, "m"))
    return density


@default_units(h=ureg.meter)
def pressure(h: Any) -> pint.Quantity:
    """Pressure of ISA atmosphere

    :param h: the altitude (by default in meters), :math:`0 < h < 84852`
        (will be clipped when outside range, integer input allowed)

    :return: the pressure, in Pa

    """
    temp = temperature(h)
    temp_0 = temperature(Q_(0, "m"))
    delta = np.maximum(Q_(0, "m"), h - H_TROP)

    press: pint.Quantity = np.where(
        h < H_TROP,
        P_0 * (temp / temp_0) ** (-G_0 / (BETA_T * R)),
        TROPOPAUSE_PRESS * np.exp(-G_0 / (R * STRATOSPHERE_TEMP) * delta),
    )
    return press


@default_units(h=ureg.meter)
def atmosphere(h: Any) -> Tuple[pint.Quantity, pint.Quantity, pint.Quantity]:
    """Pressure of ISA atmosphere

    :param h: the altitude (by default in meters), :math:`0 < h < 84852`
        (will be clipped when outside range, integer input allowed)

    :return: a tuple (pressure, density, temperature)

    """
    temp: pint.Quantity = np.maximum(
        Q_(288.15, "K") - Q_(0.0065, "K/m") * h,
        STRATOSPHERE_TEMP,
    )
    density_troposphere = RHO_0 * (temp / Q_(288.15, "K")) ** 4.256848
    delta = np.maximum(Q_(0, "m"), h - Q_(11000, "m"))
    den: pint.Quantity = density_troposphere * np.exp(
        -delta / Q_(6341.5522, "m")
    )
    temp_0 = temperature(Q_(0, "m"))
    press: pint.Quantity = np.where(
        h < H_TROP,
        P_0 * (temp / temp_0) ** (-G_0 / (BETA_T * R)),
        TROPOPAUSE_PRESS * np.exp(-G_0 / (R * STRATOSPHERE_TEMP) * delta),
    )
    return press, den, temp


@default_units(h=ureg.meter)
def sound_speed(h: Any) -> pint.Quantity:
    """Speed of sound in ISA atmosphere

    :param h: the altitude (by default in meters), :math:`0 < h < 84852`
        (will be clipped when outside range, integer input allowed)

    :return: the speed of sound :math:`a`, in m/s

    """
    temp = temperature(h)
    a = np.sqrt(GAMMA * R * temp)
    return a
