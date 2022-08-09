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
