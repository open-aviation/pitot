# pitot

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
