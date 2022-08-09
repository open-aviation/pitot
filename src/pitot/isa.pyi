# flake8: noqa

from typing import List, Union, overload

import pint
from typing_extensions import Protocol

from .types import Scalar, Array, QuantityOrArray, QuantityOrScalar

class ISA_Method(Protocol):
    @overload
    def __call__(self, h: QuantityOrArray) -> pint.Quantity[Array]: ...
    @overload
    def __call__(self, h: QuantityOrScalar) -> pint.Quantity[Scalar]: ...

temperature: ISA_Method
density: ISA_Method
pressure: ISA_Method
sound_speed: ISA_Method
