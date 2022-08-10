# flake8: noqa

from typing import Tuple, overload

import pandas as pd
import pint
from typing_extensions import Protocol

from .types import Array, QuantityOrArray, QuantityOrScalar, Scalar

class ISA_Method(Protocol):
    @overload
    def __call__(self, h: QuantityOrArray) -> pint.Quantity[Array]: ...
    @overload
    def __call__(self, h: QuantityOrScalar) -> pint.Quantity[Scalar]: ...
    @overload
    def __call__(self, h: pd.Series) -> pd.Series: ...

GAMMA: pint.Quantity[float]
P_0: pint.Quantity[float]
R: pint.Quantity[float]
RHO_0: pint.Quantity[float]
SPECIFIC_GAS_CONSTANT: pint.Quantity[float]
STRATOSPHERE_TEMP: pint.Quantity[float]

temperature: ISA_Method
density: ISA_Method
pressure: ISA_Method
sound_speed: ISA_Method

@overload
def atmosphere(
    h: QuantityOrArray,
) -> Tuple[
    pint.Quantity[Array],
    pint.Quantity[Array],
    pint.Quantity[Array],
]: ...
@overload
def atmosphere(
    h: QuantityOrScalar,
) -> Tuple[
    pint.Quantity[Scalar],
    pint.Quantity[Scalar],
    pint.Quantity[Scalar],
]: ...
