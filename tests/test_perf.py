# #%%

# import timeit

# import numpy as np
# import pandas as pd
# from openap import aero as ae
# from pint_pandas import PintArray

# from pitot import Q_, aero, isa


# def test_perf() -> None:

#     print()
#     alt = np.random.rand() * 11000
#     # array = PintArray.from_1darray_quantity(Q_(alt, "m"))
#     pds = pd.Series(alt, dtype="pint[ft]")

#     def temperature():

#         temp = isa.temperature(Q_(alt, "m"))

#     print(
#         f"- time for temperature:
# {timeit.timeit(temperature, number=119600)}s"
#     )

#     def temperature_pd():
#         temp = isa.temperature(pds)

#     print(
#         f"- time for temperature de pd:
# {timeit.timeit(temperature_pd, number=119600)}s"
#     )

#     def temperature_ft():
#         temp = isa.temperature(Q_(alt * 36089.24, "ft"))

#     print(
#         f"- time for temperature (wrong unit):
# {timeit.timeit(temperature_ft, number=119600)}s"
#     )

#     def temperature_aero():
#         temp = ae.temperature(alt * 36089.24)

#     print(
#         f"- time for temperature (without unit):
# {timeit.timeit(temperature_aero, number=119600)}s"
#     )

#     def pressure():
#         alt = np.random.rand() * 11000
#         press = isa.pressure(Q_(alt, "m"))

#     print(f"- time for pressure: {timeit.timeit(pressure, number=18886)}s")

#     def pressure_ft():
#         alt = np.random.rand() * 36089.24
#         press = isa.pressure(Q_(alt, "ft"))

#     print(
#         f"- time for pressure (wrong unit):
# {timeit.timeit(pressure_ft, number=18886)}s"
#     )

#     def tas2mach():
#         alt = np.random.rand() * 36089.24
#         tas = np.random.rand() * 400
#         press = aero.tas2mach(Q_(tas, "kts"), Q_(alt, "ft"))

#     print(
#         f"- time for tas2mach convertion:
# {timeit.timeit(tas2mach, number=33480)}s"
#     )

#     def tas2mach_si():
#         alt = np.random.rand() * 11000
#         tas = np.random.rand() * 680
#         press = aero.tas2mach(Q_(tas, "m/s"), Q_(alt, "m"))

#     print(
#         f"- time for tas2mach convertion (wrong unit):
# {timeit.timeit(tas2mach_si, number=33480)}s"
#     )

#     def get_drag_with():
#         mach = Q_(np.random.rand() * 2)
#         dP = Q_(np.random.rand())
#         s = Q_(np.random.rand() * 100 + 100, "m^2")
#         cd = Q_(np.random.rand())
#         result = 1 / 2 * dP * isa.P_0.m * isa.GAMMA.m * s * mach * mach * cd
#         return Q_(result, "N")

#     def get_drag_without(self, mach, dP, s, cd):
#         mach, dP, s, cd = np.random.rand()
#         mach, dP, s, cd = np.random.rand()
#         mach, dP, s, cd = np.random.rand()
#         mach, dP, s, cd = np.random.rand()
#         result = 1 / 2 * dP * isa.P_0.m * isa.GAMMA.m * s * mach * mach * cd
#         return Q_(result, "N")


# #%%
