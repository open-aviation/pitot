from __future__ import annotations

import functools
import inspect
import logging
from typing import Any, Callable

import numpy as np
import pandas as pd
import pint
from pint_pandas import PintArray, PintType

from . import Q_, ureg

_log = logging.getLogger(__name__)

PintType.ureg = ureg
PintType.ureg.default_format = "~P"

STRATOSPHERE_TEMP = Q_(216.65, ureg.K)  # until altitude = 22km
SPECIFIC_GAS_CONSTANT = Q_(287.05287, ureg.J / ureg.kg / ureg.K)

ReturnQuantity = Callable[..., pint.Quantity[Any]]


def default_units(**unit_kw: str | pint.Unit) -> Callable[..., ReturnQuantity]:
    def wrapper(fun: ReturnQuantity) -> ReturnQuantity:
        msg = "Input argument '{arg}' will be considered as '{unit}'"

        @functools.wraps(fun)
        def decorated_func(*args: Any, **kwargs: Any) -> pint.Quantity[Any]:
            bind_args = inspect.signature(fun).bind(*args, **kwargs)
            new_args = dict(bind_args.arguments)
            for arg, value in new_args.items():
                unit = unit_kw.get(arg, None)

                if (
                    unit is None
                    or isinstance(value, pint.Quantity)
                    or isinstance(value, PintArray)
                ):
                    continue

                if isinstance(value, pd.Series):
                    if isinstance(value.dtype, PintType):
                        new_args[arg] = value.values
                        continue
                    else:
                        value = value.values

                _log.warning(msg.format(arg=arg, unit=unit))
                new_args[arg] = Q_(value, unit)

            return fun(**new_args)

        return decorated_func

    return wrapper


@default_units(h=ureg.meter)
def temperature(h: Any) -> pint.Quantity[Any]:
    temp = np.maximum(
        Q_(288.15, ureg.K) - Q_(0.0065, ureg.K / ureg.meter) * h,
        STRATOSPHERE_TEMP,
    )
    return temp  # type: ignore


@default_units(h=ureg.meter)
def density(h: Any) -> pint.Quantity[Any]:
    temp = temperature(h)
    density_troposphere = (
        Q_(1.225, ureg.kg / ureg.meter**3)
        * (temp / Q_(288.15, ureg.K)) ** 4.256848
    )
    delta = np.maximum(Q_(0, ureg.meter), h - Q_(11000, ureg.meter))
    density: pint.Quantity[Any] = density_troposphere * np.exp(
        -delta / Q_(6341.5522, ureg.meter)
    )
    return density


@default_units(h=ureg.meter)
def pressure(h: Any) -> pint.Quantity[Any]:
    temp = temperature(h)
    den = density(h)
    press: pint.Quantity[Any] = den * temp * SPECIFIC_GAS_CONSTANT
    return press
