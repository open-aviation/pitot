from typing import Any, Tuple

from impunity import impunity
from typing_extensions import Annotated

import numpy as np

__all__ = ["temperature", "density", "pressure", "sound_speed"]

m = Annotated[Any, "meters"]

# Cp/Cv for air
GAMMA: Annotated[float, "dimensionless"] = 1.40
# sea level pressure ISA
P_0: Annotated[float, "Pa"] = 101325.0
# gas constant, sea level ISA
R: Annotated[float, "m^2 / (s^2 * K)"] = 287.05287
# sea level density ISA
RHO_0: Annotated[float, "kg / m^3"] = 1.225
# until altitude = 22km
STRATOSPHERE_TEMP: Annotated[float, "K"] = 216.65
# Gravitational acceleration
G_0: Annotated[float, "m / s^2"] = 9.80665
# Temperature gradient below tropopause, ISA
BETA_T: Annotated[float, "K / m"] = -0.0065
# pressure at tropopause, ISA
TROPOPAUSE_PRESS: Annotated[float, "Pa"] = 22632.0401
# tropopause altitude
H_TROP: Annotated[int, "m"] = 11000
# sea level altitude
SEA_ALT: Annotated[Any, "m"] = 0


@impunity
def temperature(h: Annotated[Any, "m"]) -> Annotated[Any, "K"]:
    """Temperature of ISA atmosphere

    :param h: the altitude (by default in meters), :math:`0 < h < 84852`
        (will be clipped when outside range, integer input allowed)

    :return: the temperature (in K)

    """

    temp_0: Annotated[Any, "K"] = 288.15
    c: Annotated[Any, "K/m"] = 0.0065
    temp: Annotated[Any, "K"] = np.maximum(
        temp_0 - c * h,
        STRATOSPHERE_TEMP,
    )
    return temp


@impunity
def density(h: Annotated[Any, "m"]) -> Annotated[Any, "kg * m^-3"]:
    """Density of ISA atmosphere

    :param h: the altitude (by default in meters), :math:`0 < h < 84852`
        (will be clipped when outside range, integer input allowed)

    :return: the density :math:`\\rho`, in kg/m3

    """
    temp: Annotated[Any, "K"] = temperature(h)
    temp_0: Annotated[Any, "K"] = 288.15
    density_troposphere: Annotated[Any, "kg * m^-3"] = (
        RHO_0 * (temp / temp_0) ** 4.256848
    )
    delta: Annotated[Any, "dimensionless"] = np.maximum(0, h - H_TROP)
    density: Annotated[Any, "kg * m^-3"] = density_troposphere * np.exp(
        -delta / 6341.5522
    )
    return density


@impunity
def pressure(h: Annotated[Any, "m"]) -> Annotated[Any, "Pa"]:
    """Pressure of ISA atmosphere

    :param h: the altitude (by default in meters), :math:`0 < h < 84852`
        (will be clipped when outside range, integer input allowed)

    :return: the pressure, in Pa

    """
    temp: Annotated[Any, "K"] = temperature(h)
    temp_0: Annotated[Any, "K"] = temperature(SEA_ALT)
    delta: Annotated[Any, "dimensionless"] = np.maximum(0, h - H_TROP)

    press: Annotated[Any, "Pa"] = np.where(
        h < H_TROP,
        P_0 * (temp / temp_0) ** (-G_0 / (BETA_T * R)),
        TROPOPAUSE_PRESS * np.exp(-G_0 / (R * STRATOSPHERE_TEMP) * delta),
    )
    return press


@impunity
def atmosphere(
    h: Annotated[Any, "m"]
) -> Tuple[
    Annotated[Any, "Pa"],
    Annotated[Any, "kg * m^-3"],
    Annotated[Any, "K"],
]:
    """Pressure of ISA atmosphere

    :param h: the altitude (by default in meters), :math:`0 < h < 84852`
        (will be clipped when outside range, integer input allowed)

    :return: a tuple (pressure, density, temperature)

    """
    temp: Annotated[Any, "K"] = np.maximum(
        288.15 - 0.0065 * h,
        STRATOSPHERE_TEMP,
    )
    temp_0: Annotated[Any, "K"] = temperature(SEA_ALT)

    density_troposphere: Annotated[Any, "kg * m^-3"] = (
        RHO_0 * (temp / temp_0) ** 4.256848
    )
    delta: Annotated[Any, "dimensionless"] = np.maximum(0, h - 11000)
    den: Annotated[Any, "kg * m^-3"] = density_troposphere * np.exp(
        -delta / 6341.5522
    )
    press: Annotated[Any, "Pa"] = np.where(
        h < H_TROP,
        P_0 * (temp / temp_0) ** (-G_0 / (BETA_T * R)),
        TROPOPAUSE_PRESS * np.exp(-G_0 / (R * STRATOSPHERE_TEMP) * delta),
    )
    return press, den, temp


@impunity
def sound_speed(h: Annotated[Any, "m"]) -> Annotated[Any, "m/s"]:
    """Speed of sound in ISA atmosphere

    :param h: the altitude (by default in meters), :math:`0 < h < 84852`
        (will be clipped when outside range, integer input allowed)

    :return: the speed of sound :math:`a`, in m/s

    """
    temp: Annotated[Any, "K"] = temperature(h)
    a: Annotated[Any, "m/s"] = np.sqrt(GAMMA * R * temp)
    return a
