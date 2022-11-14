from __future__ import annotations

import ast
import functools
import inspect
import logging
import textwrap
from typing import Any, Callable

import astor
import pandas as pd
import pint
import sys
from pint_pandas import PintArray, PintType

from . import Q_
from .couscous import Visitor

ReturnQuantity = Callable[..., pint.Quantity]

_log = logging.getLogger(__name__)


def default_units(**unit_kw: str | pint.Unit) -> Callable[..., ReturnQuantity]:
    def wrapper(fun: ReturnQuantity) -> ReturnQuantity:
        msg = "Default unit [{unit}] will be used for argument '{arg}'."

        @functools.wraps(fun)
        def decorated_func(*args: Any, **kwargs: Any) -> pint.Quantity:
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
                return pd.Series(array)

            return res

        return decorated_func

    return wrapper


def couscous(fun: Callable) -> Callable:
    """Decorator function to check units based on annotations

    Args:
        fun (function): decorated function

    Returns:
<<<<<<< HEAD
        new_fun (function): new function based on input
        function with eventually modified
=======
        new_fun (function): new function based on input function with eventually modified
>>>>>>> it's couscous time !
        code to keep unit coherence.
    """

    fun_tree = ast.parse(
        textwrap.dedent(inspect.getsource(fun))  # dedent for nested methods
    )  # get the function AST
<<<<<<< HEAD
    visitor = Visitor(fun)
=======
    visitor = Visitor(fun.__globals__)
>>>>>>> it's couscous time !
    fun_tree = visitor.visit(fun_tree)  # send it to the NodeTransformer
    f_str = astor.to_source(
        fun_tree
    )  # get the string of the transformed function
<<<<<<< HEAD
=======
    _log.warning(f_str)
>>>>>>> it's couscous time !
    exec(f_str[f_str.find("\n") + 1 :], fun.__globals__, locals())

    new_fun = locals()[fun.__name__]

    co_consts = new_fun.__code__.co_consts
    for const in fun.__code__.co_consts:
        if const not in co_consts:
            co_consts = co_consts + (const,)
    cocode = new_fun.__code__.co_code

    fun.__code__ = fun.__code__.replace(
        co_code=cocode,
        co_consts=co_consts,
    )

    return fun
