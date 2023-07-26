from typing import Any, Sequence, overload

from typing_extensions import Annotated

import numpy as np
import numpy.typing as npt

@overload
def distance(
    lat1: Annotated[float, "degree"],
    lon1: Annotated[float, "degree"],
    lat2: Annotated[float, "degree"],
    lon2: Annotated[float, "degree"],
    *args: Any,
    **kwargs: Any,
) -> Annotated[float, "m"]: ...
@overload
def distance(
    lat1: Annotated[Sequence[float] | npt.NDArray[np.float64], "degree"],
    lon1: Annotated[Sequence[float] | npt.NDArray[np.float64], "degree"],
    lat2: Annotated[Sequence[float] | npt.NDArray[np.float64], "degree"],
    lon2: Annotated[Sequence[float] | npt.NDArray[np.float64], "degree"],
    *args: Any,
    **kwargs: Any,
) -> Annotated[npt.NDArray[np.float64], "m"]: ...
@overload
def bearing(
    lat1: Annotated[float, "degree"],
    lon1: Annotated[float, "degree"],
    lat2: Annotated[float, "degree"],
    lon2: Annotated[float, "degree"],
    *args: Any,
    **kwargs: Any,
) -> Annotated[float, "degree"]: ...
@overload
def bearing(
    lat1: Annotated[Sequence[float] | npt.NDArray[np.float64], "degree"],
    lon1: Annotated[Sequence[float] | npt.NDArray[np.float64], "degree"],
    lat2: Annotated[Sequence[float] | npt.NDArray[np.float64], "degree"],
    lon2: Annotated[Sequence[float] | npt.NDArray[np.float64], "degree"],
    *args: Any,
    **kwargs: Any,
) -> Annotated[npt.NDArray[np.float64], "degree"]: ...
@overload
def destination(
    lat: Annotated[float, "degree"],
    lon: Annotated[float, "degree"],
    bearing: Annotated[float, "degree"],
    distance: Annotated[float, "m"],
    *args: Any,
    **kwargs: Any,
) -> tuple[
    Annotated[float, "degree"],
    Annotated[float, "degree"],
    Annotated[float, "degree"],
]: ...
@overload
def destination(
    lon: Annotated[float | Sequence[float] | npt.NDArray[np.float64], "degree"],
    lat: Annotated[float | Sequence[float] | npt.NDArray[np.float64], "degree"],
    bearing: Annotated[
        float | Sequence[float] | npt.NDArray[np.float64], "degree"
    ],
    distance: Annotated[Sequence[float] | npt.NDArray[np.float64], "m"],
    *args: Any,
    **kwargs: Any,
) -> tuple[
    Annotated[npt.NDArray[np.float64], "degree"],
    Annotated[npt.NDArray[np.float64], "degree"],
    Annotated[npt.NDArray[np.float64], "degree"],
]: ...
@overload
def destination(
    lon: Annotated[Sequence[float] | npt.NDArray[np.float64], "degree"],
    lat: Annotated[Sequence[float] | npt.NDArray[np.float64], "degree"],
    bearing: Annotated[
        float | Sequence[float] | npt.NDArray[np.float64], "degree"
    ],
    distance: Annotated[float | Sequence[float] | npt.NDArray[np.float64], "m"],
    *args: Any,
    **kwargs: Any,
) -> tuple[
    Annotated[npt.NDArray[np.float64], "degree"],
    Annotated[npt.NDArray[np.float64], "degree"],
    Annotated[npt.NDArray[np.float64], "degree"],
]: ...
def greatcircle(
    lat1: Annotated[float, "degree"],
    lon1: Annotated[float, "degree"],
    lat2: Annotated[float, "degree"],
    lon2: Annotated[float, "degree"],
    *args: Any,
    **kwargs: Any,
) -> list[tuple[Annotated[float, "degree"], Annotated[float, "degree"]]]: ...
