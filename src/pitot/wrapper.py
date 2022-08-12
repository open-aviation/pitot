from __future__ import annotations

import functools
import inspect
import logging
from typing import Any, Callable

import pandas as pd
import pint
from pint_pandas import PintArray, PintType

from . import Q_

ReturnQuantity = Callable[..., pint.Quantity[Any]]

_log = logging.getLogger(__name__)


def default_units(**unit_kw: str | pint.Unit) -> Callable[..., ReturnQuantity]:
    def wrapper(fun: ReturnQuantity) -> ReturnQuantity:
        msg = "Default unit [{unit}] will be used for argument '{arg}'."

        @functools.wraps(fun)
        def decorated_func(*args: Any, **kwargs: Any) -> pint.Quantity[Any]:
            return_pandas = False
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
                    return_pandas = True
                    if isinstance(value.dtype, PintType):
                        new_args[arg] = value.values
                        continue
                    else:
                        value = value.values

                _log.warning(msg.format(arg=arg, unit=unit))
                new_args[arg] = Q_(value, unit)

            res = fun(**new_args)

            if return_pandas and isinstance(res, pint.Quantity):
                array = PintArray.from_1darray_quantity(res)
                return pd.Series(array)  # type: ignore

            return res

        return decorated_func

    return wrapper
