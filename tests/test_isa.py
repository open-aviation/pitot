# from pathlib import Path
# from typing import TYPE_CHECKING

# import pandas as pd
# import pint
# import pytest

# from pitot import Q_, isa, ureg
# from pitot.types import Array

# if TYPE_CHECKING:
#     from pitot.isa import ISA_Method


# @pytest.fixture
# def isa_table() -> pd.DataFrame:
#     return (
#         pd.read_fwf(Path(__file__).parent / "isa_table.txt", header=[0, 1])
#         .pint.quantify(level=-1)
#         .assign(density=lambda df: isa.RHO_0 * df.density_ratio)
#     )


# @pytest.fixture
# def zero_values(isa_table: pd.DataFrame) -> pd.Series:
#     return isa_table.query("altitude == 0").iloc[0]


# @pytest.mark.parametrize(
#     "quantity,method",
#     [
#         ("density", isa.density),
#         ("pressure", isa.pressure),
#         ("sound_speed", isa.sound_speed),
#         ("temperature", isa.temperature),
#     ],
# )
# def test_quantity(
#     quantity: str,
#     method: "ISA_Method",
#     isa_table: pd.DataFrame,
#     zero_values: pd.Series,
# ) -> None:

#     # this is a regular NumPy array with altitudes in feet
#     altitude_ft: Array = isa_table.pint.dequantify().altitude.ft.values
#     expected: pint.Quantity[Array] = isa_table[quantity].values.quantity

#     r1 = method(Q_(0, ureg.m))  # value with unit
#     assert r1.m == pytest.approx(zero_values[quantity].to(r1.u).m, rel=1e-2)

#     r2 = method(0)  # value without unit
#     assert r2.m == pytest.approx(zero_values[quantity].to(r2.u).m, rel=1e-2)

#     r3 = method(Q_(altitude_ft, ureg.ft))  # numpy array with unit
#     assert r3.m == pytest.approx(expected.to(r3.u).m, rel=1e-2)

#     r4 = method(0.3048 * altitude_ft)  # regular numpy array
#     assert r4.m == pytest.approx(expected.to(r4.u).m, rel=1e-2)

#     r5 = method(isa_table["altitude"])  # pandas Series with unit
#     assert r5.values.quantity.m == pytest.approx(
#         expected.to(r5.dtype.units).m, rel=1e-2
#     )

#     r6 = method(0.3048 * pd.Series(altitude_ft))  # pandas Series without unit
#     assert r6.values.quantity.m == pytest.approx(
#         expected.to(r6.dtype.units).m, rel=1e-2
#     )
