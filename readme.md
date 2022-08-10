# pitot

[![tests](https://github.com/atmdata/pitot/actions/workflows/run-tests.yml/badge.svg)](https://github.com/atmdata/pitot/actions/workflows/run-tests.yml)
[![Code Coverage](https://img.shields.io/codecov/c/github/atmtdata/pitot.svg)](https://codecov.io/gh/atmdata/pitot)
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
