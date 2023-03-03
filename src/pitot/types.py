from typing import Sequence, Union

import pint

import numpy as np
import numpy.typing as npt

Scalar = Union[int, float, np.float_]
QuantityOrScalar = Union[Scalar, pint.Quantity]

# It is still difficult to include PintArray as they are seen as `Any`.
Array = npt.NDArray[np.float_]
QuantityOrArray = Union[Sequence[float], Array, pint.Quantity]
