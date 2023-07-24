"""
This module contains a set of geodesy functions wrapped around all what is
available in the `pyproj <https://pyproj4.github.io/pyproj/stable/>`_ library.
All angles are in degrees, all distances are in meter.
"""
from __future__ import annotations

from typing import Any, List, Tuple

from impunity import impunity
from typing_extensions import Annotated

from pyproj import Geod


@impunity
def distance(
    lat1: Annotated[Any, "degree"],
    lon1: Annotated[Any, "degree"],
    lat2: Annotated[Any, "degree"],
    lon2: Annotated[Any, "degree"],
    *args: Annotated[Any, "dimensionless"],
    **kwargs: Annotated[Any, "dimensionless"],
) -> Annotated[Any, "m"]:
    """Computes the distance(s) between two points (or arrays of points).

    :param lat1: latitude value(s)
    :param lon1: longitude value(s)
    :param lat2: latitude value(s)
    :param lon2: longitude value(s)

    :return: the distance, in meters

    """
    geod = Geod(ellps="WGS84")
    dist1: Annotated[Any, "m"]
    _, _, dist1 = geod.inv(lon1, lat1, lon2, lat2, *args, **kwargs)
    return dist1


@impunity
def bearing(
    lat1: Annotated[Any, "degree"],
    lon1: Annotated[Any, "degree"],
    lat2: Annotated[Any, "degree"],
    lon2: Annotated[Any, "degree"],
    *args: Annotated[Any, "dimensionless"],
    **kwargs: Annotated[Any, "dimensionless"],
) -> Annotated[Any, "degree"]:
    """Computes the distance(s) between two points (or arrays of points).

    :param lat1: latitude value(s)
    :param lon1: longitude value(s)
    :param lat2: latitude value(s)
    :param lon2: longitude value(s)

    :return: the bearing angle, in degrees, from the first point to the second
    """
    geod = Geod(ellps="WGS84")
    angle1: Annotated[Any, "degree"]
    angle1, _, _ = geod.inv(lon1, lat1, lon2, lat2, *args, **kwargs)
    return angle1


@impunity
def destination(
    lat: Annotated[Any, "degree"],
    lon: Annotated[Any, "degree"],
    bearing: Annotated[Any, "degree"],
    distance: Annotated[Any, "m"],
    *args: Annotated[Any, "dimensionless"],
    **kwargs: Annotated[Any, "dimensionless"],
) -> Tuple[
    Annotated[Any, "degree"],
    Annotated[Any, "degree"],
    Annotated[Any, "degree"],
]:
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
    lon_: Annotated[Any, "degree"]
    lat_: Annotated[Any, "degree"]
    back_: Annotated[Any, "degree"]
    lon_, lat_, back_ = geod.fwd(lon, lat, bearing, distance, *args, **kwargs)
    return lat_, lon_, back_


@impunity
def greatcircle(
    lat1: Annotated[Any, "degree"],
    lon1: Annotated[Any, "degree"],
    lat2: Annotated[Any, "degree"],
    lon2: Annotated[Any, "degree"],
    *args: Annotated[Any, "dimensionless"],
    **kwargs: Annotated[Any, "dimensionless"],
) -> List[Annotated[Any, "degree"]]:
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
