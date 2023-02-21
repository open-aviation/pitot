import logging
from typing import Any, Tuple

import numpy as np
import pytest
from impunity import impunity  # type: ignore
from typing_extensions import Annotated

from pitot import isa
from pitot.isa import temperature

m = Annotated[Any, "m"]
ft = Annotated[Any, "ft"]
K = Annotated[Any, "K"]
Pa = Annotated[Any, "Pa"]
cm = Annotated[Any, "cm"]

# -----------------------
# du : different units
# wu : wrong units
# bin : Binary operator in func call
# -----------------------


@impunity  # type: ignore
def temperature_2(altitude_m: "m", altitude_ft: "ft") -> Tuple["K", "K"]:
    temp_m: "K" = np.maximum(288.15 - 0.0065 * altitude_m, 216.65)
    temp_ft: "K" = np.maximum(288.15 - 0.0065 * altitude_ft * 0.3048, 216.65)
    return temp_m, temp_ft


def test_base() -> None:
    @impunity  # type: ignore
    def test_base() -> None:
        alt_m: "m" = 1000
        temp = temperature(alt_m)
        assert temp == pytest.approx(281.65, rel=1e-1)

    test_base()


def test_base_cm() -> None:
    @impunity  # type: ignore
    def test_base_cm() -> None:
        alt_m: "m" = 1000
        temp = temperature(alt_m)
        assert temp == pytest.approx(281.65, rel=1e-1)

        alt_cm: "cm" = 100000
        temp = temperature(alt_cm)
        assert temp == pytest.approx(281.65, rel=1e-1)

    test_base_cm()


def test_2_params() -> None:
    @impunity  # type: ignore
    def test_2_params() -> None:
        alt_m: "m" = 1000
        alt_ft: "ft" = 1000
        temp_m = temperature_2(alt_m, alt_ft)
        assert temp_m[0] == pytest.approx(281.65, rel=1e-1)

    test_2_params()


def test_tuples() -> None:
    @impunity  # type: ignore
    def test_2_params() -> None:
        alt_m: "m" = 1000
        alt_ft: "ft" = 1000
        temp_ft, temp_m = temperature_2(alt_m, alt_ft)
        assert temp_m == pytest.approx(281.65, rel=1e-1)
        assert temp_ft == pytest.approx(286.17, rel=1e-1)

    test_2_params()


def test_different_units() -> None:
    @impunity  # type: ignore
    def test_different_units():
        alt_ft: "ft" = 1000
        temp = temperature(alt_ft)
        assert temp == pytest.approx(286.17, rel=1e-1)

    test_different_units()


def test_binOp() -> None:
    @impunity  # type: ignore
    def test_binOp() -> None:
        alt_ft: "ft" = 1000
        temp = temperature(alt_ft * 3)
        assert temp == pytest.approx(286.17, rel=1e-1)

    test_binOp()


def test_call_np() -> None:
    @impunity  # type: ignore
    def test_call_np(h: "m") -> "K":
        temp_0: "K" = 288.15
        c: Annotated[Any, "K/m"] = 0.0065
        temp: "K" = np.maximum(
            temp_0 - c * h,
            216.65,
        )
        return temp

    m2: "m" = 11000
    res = test_call_np(m2)
    assert res == pytest.approx(isa.STRATOSPHERE_TEMP, rel=1e-1)


def test_using_globals() -> None:
    @impunity  # type: ignore
    def test_using_globals(h: "m") -> "K":
        temp_0: "K" = 288.15
        c: Annotated[Any, "K/m"] = 0.0065
        e = isa.STRATOSPHERE_TEMP
        temp: "K" = np.maximum(
            temp_0 - c * h,
            e,
        )
        return temp

    m2: "m" = 11000
    res = test_using_globals(m2)
    assert res == pytest.approx(isa.STRATOSPHERE_TEMP, rel=1e-1)


def test_wrong_units(caplog) -> None:  # type: ignore
    @impunity  # type: ignore
    def test_wrong_units():
        alt_ft: "K" = 1000
        temperature(alt_ft)

    caplog.set_level(logging.WARNING)
    test_wrong_units()
    assert "WARNING" in caplog.text


def test_wrong_received_units(caplog) -> None:  # type: ignore
    @impunity  # type: ignore
    def test_wrong_received_units() -> None:
        alt_ft: "ft" = 1000
        res: "ft" = temperature(alt_ft)  # noqa F841

    caplog.set_level(logging.WARNING)
    test_wrong_received_units()
    assert "WARNING" in caplog.text
