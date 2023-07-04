# flake8: noqa

# from typing import overload

# import pandas as pd
# import pint
# from typing_extensions import Protocol

# from .types import Array, QuantityOrArray, QuantityOrScalar, Scalar

# class AeroMethod(Protocol):
#     @overload
#     def __call__(
#         self, _: QuantityOrArray, h: QuantityOrArray
#     ) -> pint.Quantity[Array]: ...
#     @overload
#     def __call__(
#         self, _: QuantityOrArray, h: QuantityOrScalar
#     ) -> pint.Quantity[Array]: ...
#     @overload
#     def __call__(
#         self, _: QuantityOrScalar, h: QuantityOrArray
#     ) -> pint.Quantity[Array]: ...
#     @overload
#     def __call__(
#         self, _: QuantityOrScalar, h: QuantityOrScalar
#     ) -> pint.Quantity[Scalar]: ...
#     # @overload
#     # def __call__(self, _: QuantityOrScalar, h: pd.Series) -> pd.Series: ...
#     # @overload
#     # def __call__(self, _: QuantityOrArray, h: pd.Series) -> pd.Series: ...
#     # @overload
#     # def __call__(self, _: pd.Series, h: QuantityOrScalar) -> pd.Series: ...
#     # @overload
#     # def __call__(self, _: pd.Series, h: QuantityOrArray) -> pd.Series: ...
#     # @overload
#     # def __call__(self, _: pd.Series, h: pd.Series) -> pd.Series: ...

# tas2mach: AeroMethod
# mach2tas: AeroMethod
# eas2tas: AeroMethod
# tas2eas: AeroMethod
# cas2tas: AeroMethod
# tas2cas: AeroMethod
# mach2cas: AeroMethod
# cas2mach: AeroMethod
