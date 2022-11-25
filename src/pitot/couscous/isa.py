from typing_extensions import Annotated
from typing import Any, Tuple

import numpy as np

from .. import Q_
from ..wrapper import couscous

__all__ = ["temperature", "density", "pressure", "sound_speed"]

Pa = s = m = kg = K = J = dimensionless = Any

GAMMA = 1.40  # Cp/Cv for air
P_0: "Pa" = 101325.0  # sea level pressure ISA
R: "m^2 / (s^2 * K)" = 287.05287  # gas constant, sea level ISA
RHO_0: "kg / m^3" = 1.225  # sea level density ISA
STRATOSPHERE_TEMP: Annotated[float, "K"] = 216.65  # until altitude = 22km
G_0: "m / s^2" = 9.80665  # Gravitational acceleration
BETA_T: "K / m" = -0.0065  # Temperature gradient below tropopause, ISA
TROPOPAUSE_PRESS: "Pa" = 22632.0401  # pressure at tropopause, ISA
H_TROP: "m" = 11000  # tropopause altitude


@couscous
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


@couscous
def density(h: "m") -> "kg * m^-3":
    """Density of ISA atmosphere

    :param h: the altitude (by default in meters), :math:`0 < h < 84852`
        (will be clipped when outside range, integer input allowed)

    :return: the density :math:`\\rho`, in kg/m3

    """
    temp: "K" = temperature(h)
    density_troposphere: "kg * m^-3" = RHO_0 * (temp / 288.15) ** 4.256848
    delta: "dimensionless" = np.maximum(0, h - H_TROP)
    density: "kg * m^-3" = density_troposphere * np.exp(-delta / 6341.5522)
    return density


@couscous
def pressure(h: Annotated[float, "m"]) -> "Pa":
    """Pressure of ISA atmosphere

    :param h: the altitude (by default in meters), :math:`0 < h < 84852`
        (will be clipped when outside range, integer input allowed)

    :return: the pressure, in Pa

    """
    temp: "K" = temperature(h)
    temp_0: "K" = temperature(0)
    delta = np.maximum(0, h - H_TROP)

    press: "Pa" = np.where(
        h < H_TROP,
        P_0 * (temp / temp_0) ** (-G_0 / (BETA_T * R)),
        TROPOPAUSE_PRESS * np.exp(-G_0 / (R * STRATOSPHERE_TEMP) * delta),
    )
    return press


@couscous
def atmosphere(h: Annotated[float, "m"]) -> Tuple["Pa", "kg * m^-3", "K"]:
    """Pressure of ISA atmosphere

    :param h: the altitude (by default in meters), :math:`0 < h < 84852`
        (will be clipped when outside range, integer input allowed)

    :return: a tuple (pressure, density, temperature)

    """
    temp: "K" = np.maximum(
        288.15 - 0.0065 * h,
        STRATOSPHERE_TEMP,
    )
    density_troposphere: "kg * m^-3" = RHO_0 * (temp / 288.15) ** 4.256848
    delta: "dimensionless" = np.maximum(0, h - 11000)
    den: "kg * m^-3" = density_troposphere * np.exp(-delta / 6341.5522)
    temp_0: "K" = temperature(Q_(0, "m"))
    press: "Pa" = np.where(
        h < H_TROP,
        P_0 * (temp / temp_0) ** (-G_0 / (BETA_T * R)),
        TROPOPAUSE_PRESS * np.exp(-G_0 / (R * STRATOSPHERE_TEMP) * delta),
    )
    return press, den, temp


@couscous
def sound_speed(h: "m") -> "m/s":
    """Speed of sound in ISA atmosphere

    :param h: the altitude (by default in meters), :math:`0 < h < 84852`
        (will be clipped when outside range, integer input allowed)

    :return: the speed of sound :math:`a`, in m/s

    """
    temp: "K" = temperature(h)
    a: "m/s" = np.sqrt(GAMMA * R * temp)
    return a
