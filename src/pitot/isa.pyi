# flake8: noqa

from typing import Union, overload

import numpy as np
import numpy.typing as npt
import pandas as pd
import pint
from pint_pandas import PintArray

Scalar = Union[int, float, np.float_]
QuantityOrScalar = Union[
    Scalar,
    pint.Quantity[int],
    pint.Quantity[float],
    pint.Quantity[np.float_],
]
Array = npt.NDArray[np.float_]
QuantityOrArray = Union[Array, pint.Quantity[Array], PintArray, pd.Series]

# The `type: ignore` instructions below are necessary as long as mypy sees
# PintArray and pd.Series as Any.

@overload
def temperature(h: QuantityOrScalar) -> pint.Quantity[Scalar]: ...  # type: ignore
@overload
def temperature(h: QuantityOrArray) -> pint.Quantity[Array]: ...
@overload
def density(h: QuantityOrScalar) -> pint.Quantity[Scalar]: ...  # type: ignore
@overload
def density(h: QuantityOrArray) -> pint.Quantity[Array]: ...
@overload
def pressure(h: QuantityOrScalar) -> pint.Quantity[Scalar]: ...  # type: ignore
@overload
def pressure(h: QuantityOrArray) -> pint.Quantity[Array]: ...
