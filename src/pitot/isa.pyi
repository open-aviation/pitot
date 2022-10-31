# flake8: noqa

from typing import Tuple, overload

import pandas as pd
import pint
from typing_extensions import Protocol

from .types import Array, QuantityOrArray, QuantityOrScalar, Scalar

class ISA_Method(Protocol):
    # @overload
    def __call__(self, h: QuantityOrArray) -> pint.Quantity: ...
    # @overload
    # def __call__(self, h: pd.Series) -> pd.Series: ...

GAMMA: pint.Quantity
P_0: pint.Quantity
R: pint.Quantity
RHO_0: pint.Quantity
SPECIFIC_GAS_CONSTANT: pint.Quantity
STRATOSPHERE_TEMP: pint.Quantity
G_0: pint.Quantity
BETA_T: pint.Quantity
TROPOPAUSE_PRESS: pint.Quantity
H_TROP: pint.Quantity

temperature: ISA_Method
density: ISA_Method
pressure: ISA_Method
sound_speed: ISA_Method

def atmosphere(
    h: QuantityOrArray,
) -> Tuple[pint.Quantity, pint.Quantity, pint.Quantity,]: ...
