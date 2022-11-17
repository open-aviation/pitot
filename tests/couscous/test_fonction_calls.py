from typing import Any, Tuple
import pytest
from pitot.wrapper import couscous
from pitot.couscous.isa import STRATOSPHERE_TEMP
import pint
import numpy as np

m = K = ft = cm = Any

# -----------------------
# du : different units
# wu : wrong units
# bin : Binary operator in func call
# -----------------------


def temperature(altitude_m: "m") -> "K":
    temp: pint.Quantity[Any] = np.maximum(288.15 - 0.0065 * altitude_m, 216.65)
    return temp


def temperature_2(altitude_m: "m", altitude_ft: "ft") -> Tuple["K", "K"]:
    temp_m: pint.Quantity[Any] = np.maximum(
        288.15 - 0.0065 * altitude_m, 216.65
    )
    temp_ft: pint.Quantity[Any] = np.maximum(
        288.15 - 0.0065 * altitude_ft * 0.3048, 216.65
    )
    return temp_m, temp_ft


def test_base():
    @couscous
    def test_base():

        alt_m: "m" = 1000
        temp = temperature(alt_m)
        assert temp == pytest.approx(281.65, rel=1e-1)

    test_base()


def test_base_cm():
    @couscous
    def test_base_cm():

        alt_m: "m" = 1000
        temp = temperature(alt_m)
        assert temp == pytest.approx(281.65, rel=1e-1)

        alt_cm: "cm" = 100000
        temp = temperature(alt_cm)
        assert temp == pytest.approx(281.65, rel=1e-1)

    test_base_cm()


def test_2_params():
    @couscous
    def test_2_params():

        alt_m: "m" = 1000
        alt_ft: "ft" = 1000
        temp_m = temperature_2(alt_m, alt_ft)
        assert temp_m[0] == pytest.approx(281.65, rel=1e-1)

    test_2_params()


def test_tuples():
    @couscous
    def test_2_params():

        alt_m: "m" = 1000
        alt_ft: "ft" = 1000
        temp_ft, temp_m = temperature_2(alt_m, alt_ft)
        assert temp_m == pytest.approx(281.65, rel=1e-1)
        assert temp_ft == pytest.approx(286.17, rel=1e-1)

    test_2_params()


def test_different_units():
    @couscous
    def test_different_units():
        alt_ft: "ft" = 1000
        temp = temperature(alt_ft)
        assert temp == pytest.approx(286.17, rel=1e-1)

    test_different_units()


def test_binOp():
    @couscous
    def test_binOp():
        alt_ft: "ft" = 1000
        temp = temperature(alt_ft * 3)
        assert temp == pytest.approx(286.17, rel=1e-1)

    test_binOp()


def test_call_np():
    @couscous
    def test_call_np(h: "m") -> "K":

        temp_0: "K" = 288.15
        c: "K/m" = 0.0065
        temp: "K" = np.maximum(
            temp_0 - c * h,
            216.65,
        )
        return temp

    m: "m" = 11000
    res = test_call_np(m)
    assert res == pytest.approx(STRATOSPHERE_TEMP, rel=1e-1)


def test_using_globals():
    @couscous
    def test_using_globals(h: "m") -> "K":

        temp_0: "K" = 288.15
        c: "K/m" = 0.0065
        temp: "K" = np.maximum(
            temp_0 - c * h,
            STRATOSPHERE_TEMP,
        )
        return temp

    m: "m" = 11000
    res = test_using_globals(m)
    assert res == pytest.approx(STRATOSPHERE_TEMP, rel=1e-1)


def test_wrong_units():
    @couscous
    def test_wrong_units():
        with pytest.raises(pint.errors.DimensionalityError):
            alt_ft: "K" = 1000
            temperature(alt_ft)

    test_wrong_units()


def main():
    test_wrong_units()


if __name__ == "__main__":
    main()
