# pitot

[![tests](https://github.com/atmdata/pitot/actions/workflows/run-tests.yml/badge.svg)](https://github.com/atmdata/pitot/actions/workflows/run-tests.yml)
[![Code Coverage](https://img.shields.io/codecov/c/github/atmdata/pitot.svg)](https://codecov.io/gh/atmdata/pitot)
[![Checked with mypy](https://img.shields.io/badge/mypy-checked-blue.svg)](https://mypy.readthedocs.io/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-black.svg)](https://github.com/psf/black)
![License](https://img.shields.io/pypi/l/pitot.svg)\
![PyPI version](https://img.shields.io/pypi/v/pitot)
[![PyPI downloads](https://img.shields.io/pypi/dm/pitot)](https://pypi.org/project/pitot)
![Conda version](https://img.shields.io/conda/vn/conda-forge/pitot)
[![Conda Downloads](https://img.shields.io/conda/dn/conda-forge/pitot.svg)](https://anaconda.org/conda-forge/pitot)

pitot is a Python toolbox providing efficient aeronautic calculations.

Implementations are:

- **efficient**, based on NumPy or state-of-the-art libraries;
- provided with **typing stubs**;
- unambiguous with **physical units**, with the help of the [`pint`](https://pint.readthedocs.io/) library.  
  All parameters may be passed with or without a physical unit (default units are explicit in the documentation), but all return values come with a physical unit.

The following functions are currently available:

- International Standard Atmosphere (temperature, density, pressure and speed of sound);
- conversions between various air speeds: CAS, TAS, EAS and Mach number;
- geodetic calculations (distance, bearing, great circle, etc.) on a WGS84 ellipsoid.

## Installation

### Latest release

```sh
pip install pitot
```

### Development version

```sh
poetry install
```

## Basic usage

Physical units are not mandatory for arguments, but return values are all [`pint`](https://pint.readthedocs.io/) quantities

```pycon
>>> from pitot.isa import temperature
>>> temperature(0)
Default unit [m] will be used for argument 'h'.
<Quantity(288.15, 'kelvin')>
>>> temperature([0, 1000])
Default unit [m] will be used for argument 'h'.
<Quantity([288.15 281.65], 'kelvin')>
```

You may access the value with the `m` (stands for _magnitude_) attribute:

```pycon
>>> temperature(0).m  # in Kelvin by default
Default unit [m] will be used for argument 'h'.
288.15
>>> temperature(0).to("°C").m
Default unit [m] will be used for argument 'h'.
15.0
```

It is preferable to avoid warnings by passing values with a physical unit:

```pycon
>>> from pitot import Q_
>>> temperature(Q_([0, 1000], "ft")).to("°C")
<Quantity([15.     13.0188], 'degree_Celsius')>
```

Things also work with NumPy arrays...

```pycon
>>> import numpy as np
>>> temperature(Q_(np.array([0, 1000]), "ft"))
<Quantity([288.15   286.1688], 'kelvin')>
>>> temperature(Q_(np.array([0, 1000]), "ft")).to("°C").m
array([15.    , 13.0188])
```

... or with Pandas Series:

```pycon
>>> import pandas as pd
>>> temperature(pd.Series([0., 1000], dtype="pint[ft]")).pint.to("°C")
0                  15.0
1    13.018799999999999
dtype: pint[°C]
```
