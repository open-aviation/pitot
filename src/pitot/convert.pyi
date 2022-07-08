# flake8: noqa

from typing import Union, overload

import pint

import numpy as np
import numpy.typing as npt

Scalar = Union[int, float, np.float_]
QuantityOrScalar = Union[
    Scalar,
    pint.Quantity[int],
    pint.Quantity[float],
    pint.Quantity[np.float_],
]
Array = npt.NDArray[np.float_]
QuantityOrArray = Union[Array, pint.Quantity[Array]]

@overload
def temperature(h: QuantityOrScalar) -> pint.Quantity[Scalar]: ...
@overload
def temperature(h: QuantityOrArray) -> pint.Quantity[Array]: ...
