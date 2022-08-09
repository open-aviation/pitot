from typing import Union

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

# At the moment, it is still difficult to include PintArray and pd.Series as
# they are seen as `Any`.
# For pandas, there is pandas-stubs but it includes an unnecessary upper bound
# on Python versions (<3.11 at the time we write these lines).

QuantityOrArray = Union[Array, pint.Quantity[Array]]
