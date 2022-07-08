from typing import TypeVar, Union

import numpy as np
import numpy.typing as npt
import pandas as pd
import pint

u = pint.UnitRegistry()


STRATOSPHERE_TEMP = 216.65 * u.K  # until alt=22km


Scalar = Union[float, np.float_]
Numeric = TypeVar(
    "Numeric",
    Scalar,
    pint.Quantity,
    npt.NDArray[np.float_],
    pd.Series,
)


def temperature(h: Numeric) -> Numeric:  # Numeric[u.K]
    t = np.maximum(
        288.15 * u.K - 0.0065 * u.K / u.meter * h,
        STRATOSPHERE_TEMP,
    )
    return t
