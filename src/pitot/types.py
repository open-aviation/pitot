from typing import Sequence, Union

import numpy as np
import numpy.typing as npt
import pint

Scalar = Union[int, float, np.float_]

QuantityOrScalar = Union[
    Scalar,
    pint.Quantity[int],
    pint.Quantity[float],
    pint.Quantity[np.float_],
]

Array = npt.NDArray[np.float_]

# It is still difficult to include PintArray as they are seen as `Any`.
QuantityOrArray = Union[Sequence[float], Array, pint.Quantity[Array]]
