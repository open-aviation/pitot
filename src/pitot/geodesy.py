"""
This module contains a set of geodesy functions wrapped around all what is
available in the `pyproj <https://pyproj4.github.io/pyproj/stable/>`_ library.
All angles are in degrees, all distances are in meter.
"""
from __future__ import annotations

from typing import Any

import pint
from pyproj import Geod

from . import ureg
from .wrapper import default_units


def distance(
    lat1: float,
    lon1: float,
    lat2: float,
    lon2: float,
    *args: Any,
    **kwargs: Any,
) -> Any:
    """Computes the distance(s) between two points (or arrays of points).

    :param lat1: latitude value(s)
    :param lon1: longitude value(s)
    :param lat2: latitude value(s)
    :param lon2: longitude value(s)

    :return: the distance, in meters

    """
    geod = Geod(ellps="WGS84")
    angle1, angle2, dist1 = geod.inv(lon1, lat1, lon2, lat2, *args, **kwargs)
    return dist1 * ureg.m


def bearing(
    lat1: float,
    lon1: float,
    lat2: float,
    lon2: float,
    *args: Any,
    **kwargs: Any,
) -> Any:
    """Computes the distance(s) between two points (or arrays of points).

    :param lat1: latitude value(s)
    :param lon1: longitude value(s)
    :param lat2: latitude value(s)
    :param lon2: longitude value(s)

    :return: the bearing angle, in degrees, from the first point to the second
    """
    geod = Geod(ellps="WGS84")
    angle1, angle2, dist1 = geod.inv(lon1, lat1, lon2, lat2, *args, **kwargs)
    return angle1


@default_units(distance="m")
def destination(
    lat: float,
    lon: float,
    bearing: float,
    distance: pint.Quantity[Any],
    *args: Any,
    **kwargs: Any,
) -> Any:
    """Computes the point you reach from a set of coordinates, moving in a
    given direction for a given distance.

    :param lat: latitude value(s)
    :param lon: longitude value(s)
    :param bearing: bearing value(s)
    :param distance: distance value(s)

    :return: a tuple with latitude value(s), longitude value(s) and bearing
        from the destination point back to the origin, all in degrees.
    """
    geod = Geod(ellps="WGS84")
    lon_, lat_, back_ = geod.fwd(
        lon, lat, bearing, distance.to("m").m, *args, **kwargs
    )
    return lat_, lon_, back_


def greatcircle(
    lat1: float,
    lon1: float,
    lat2: float,
    lon2: float,
    *args: Any,
    **kwargs: Any,
) -> Any:
    """Computes a list of points making the great circle between two points.

    :param lat1: latitude value
    :param lon1: longitude value
    :param lat2: latitude value
    :param lon2: longitude value

    :return: a tuple with latitude values, longitude values, all in degrees.
    """

    geod = Geod(ellps="WGS84")

    return [
        (lat, lon)
        for (lon, lat) in geod.npts(lon1, lat1, lon2, lat2, *args, **kwargs)
    ]
