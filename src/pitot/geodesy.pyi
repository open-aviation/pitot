# flake8: noqa

from typing import Any, Sequence, overload

import pint

from .types import Array, QuantityOrArray, QuantityOrScalar

@overload
def distance(
    lat1: float,
    lon1: float,
    lat2: float,
    lon2: float,
    *args: Any,
    **kwargs: Any,
) -> pint.Quantity: ...
@overload
def distance(
    lat1: Sequence[float] | Array,
    lon1: Sequence[float] | Array,
    lat2: Sequence[float] | Array,
    lon2: Sequence[float] | Array,
    *args: Any,
    **kwargs: Any,
) -> pint.Quantity: ...
@overload
def bearing(
    lat1: float,
    lon1: float,
    lat2: float,
    lon2: float,
    *args: Any,
    **kwargs: Any,
) -> float: ...
@overload
def bearing(
    lat1: Sequence[float] | Array,
    lon1: Sequence[float] | Array,
    lat2: Sequence[float] | Array,
    lon2: Sequence[float] | Array,
    *args: Any,
    **kwargs: Any,
) -> Array: ...
@overload
def destination(
    lat: float,
    lon: float,
    bearing: float,
    distance: QuantityOrScalar,
    *args: Any,
    **kwargs: Any,
) -> tuple[float, float, float]: ...
@overload
def destination(
    lat: Sequence[float] | Array,
    lon: Sequence[float] | Array,
    bearing: Sequence[float] | Array,
    distance: QuantityOrArray,
    *args: Any,
    **kwargs: Any,
) -> tuple[Array, Array, Array]: ...
def greatcircle(
    lat1: float,
    lon1: float,
    lat2: float,
    lon2: float,
    *args: Any,
    **kwargs: Any,
) -> list[tuple[float, float]]: ...
