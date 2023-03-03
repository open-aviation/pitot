import logging
from typing import Any

import pytest
from impunity import impunity  # type: ignore
from typing_extensions import Annotated

import numpy as np

m = Annotated[Any, "m"]
ft = Annotated[Any, "ft"]
K = Annotated[Any, "K"]
Pa = Annotated[Any, "Pa"]


# -----------------------
# du : different units
# wu : wrong units
# bin : Binary operator in func call
# -----------------------


def test_base() -> None:
    @impunity  # type: ignore
    def test_base() -> None:
        alt_m: "m" = 1000
        alt_m2: "m" = alt_m
        assert alt_m == alt_m2

    test_base()


def test_different_units() -> None:
    @impunity  # type: ignore
    def test_different_units() -> None:
        alt_m: "m" = 1000
        alt_ft: "ft" = alt_m
        # assert alt_m == 1000
        assert alt_ft == pytest.approx(3280.84, rel=1e-2)

    test_different_units()


def test_wrong_units(caplog) -> None:  # type: ignore
    @impunity  # type: ignore
    def test_wrong_units() -> None:
        alt_m: "m" = 1000
        alt_K: "K" = alt_m  # noqa F841

    caplog.set_level(logging.WARNING)
    test_wrong_units()
    assert "WARNING" in caplog.text


def test_assign_wo_annotation() -> None:
    @impunity  # type: ignore
    def test_assign_wo_annotation() -> None:
        density_troposphere = np.maximum(1500, 6210)  # return None unit
        density: "Pa" = density_troposphere * np.exp(0)
        assert density == 6210

    test_assign_wo_annotation()
