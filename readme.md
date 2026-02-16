# pitot

![tests](https://github.com/atmdata/pitot/actions/workflows/run-tests.yml/badge.svg)
![Code Coverage](https://img.shields.io/codecov/c/github/atmdata/pitot.svg)
![Checked with mypy](https://img.shields.io/badge/mypy-checked-blue.svg)
![Code style: black](https://img.shields.io/badge/code%20style-black-black.svg)
![License](https://img.shields.io/pypi/l/pitot.svg)\
![PyPI version](https://img.shields.io/pypi/v/pitot)
![PyPI downloads](https://img.shields.io/pypi/dm/pitot)
![Conda version](https://img.shields.io/conda/vn/conda-forge/pitot)
![Conda Downloads](https://img.shields.io/conda/dn/conda-forge/pitot.svg)

pitot is a Python toolbox providing efficient aeronautic calculations.

Implementations are:

- **efficient**, based on NumPy or state-of-the-art libraries;
- provided with **typing stubs**;
- unambiguous with **physical units**, with the help of the [`impunity`](https://achevrot.github.io/impunity/) library, based on annotations.

The following functions are currently available:

- International Standard Atmosphere (temperature, density, pressure, and speed of sound);
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

## Contributions

Any input, feedback, bug report or contribution is welcome.

Before opening a PR, please check your commits follow a number of safeguards with hooks to install as follows:

```sh
prek install -f
```
