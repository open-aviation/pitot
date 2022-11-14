from typing import Any
import pytest
from pitot.wrapper import couscous
import pint
<<<<<<< HEAD
import numpy as np

m = K = ft = Pa = Any
=======
from pitot import Q_

m = K = ft = Any
>>>>>>> it's couscous time !


# -----------------------
# du : different units
# wu : wrong units
# bin : Binary operator in func call
# -----------------------


<<<<<<< HEAD
def test_base():
    @couscous
    def test_base():
        alt_m: "m" = 1000
        alt_m2: "m" = alt_m
        assert alt_m == alt_m2

    test_base()
=======
@couscous
def test_base():

    alt_m: "m" = 1000
    alt_m2: "m" = alt_m
    assert alt_m == alt_m2
>>>>>>> it's couscous time !


def test_different_units():
    @couscous
    def test_different_units():

        alt_m: "m" = 1000
        alt_ft: "ft" = alt_m
<<<<<<< HEAD
=======
        print(alt_ft)
>>>>>>> it's couscous time !
        # assert alt_m == 1000
        assert alt_ft == pytest.approx(3280.84, rel=1e-2)

    test_different_units()


def test_wrong_units():
    @couscous
    def test_wrong_units():
<<<<<<< HEAD
        with pytest.raises(pint.errors.DimensionalityError):
            alt_m: "m" = 1000
=======

        alt_m: "m" = 1000
        with pytest.raises(pint.errors.DimensionalityError):
>>>>>>> it's couscous time !
            alt_K: "K" = alt_m

    test_wrong_units()


<<<<<<< HEAD
def test_assign_wo_annotation():
    @couscous
    def test_assign_wo_annotation():
        density_troposphere = np.maximum(1500, 6210)  # return None unit
        density: "Pa" = density_troposphere * np.exp(0)
        assert density == 6210

    test_assign_wo_annotation()


=======
>>>>>>> it's couscous time !
def main():
    test_different_units()


if __name__ == "__main__":
    main()
