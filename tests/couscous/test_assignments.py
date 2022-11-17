from typing import Any
import pytest
from pitot.wrapper import couscous
import pint

m = K = ft = Any


# -----------------------
# du : different units
# wu : wrong units
# bin : Binary operator in func call
# -----------------------


@couscous
def test_base():

    alt_m: "m" = 1000
    alt_m2: "m" = alt_m
    assert alt_m == alt_m2


def test_different_units():
    @couscous
    def test_different_units():

        alt_m: "m" = 1000
        alt_ft: "ft" = alt_m
        print(alt_ft)
        # assert alt_m == 1000
        assert alt_ft == pytest.approx(3280.84, rel=1e-2)

    test_different_units()


def test_wrong_units():
    with pytest.warns():

        @couscous
        def test_wrong_units():

            alt_m: "m" = 1000
            alt_K: "K" = alt_m
            print(alt_K)

        test_wrong_units()


def main():
    test_different_units()


if __name__ == "__main__":
    main()
