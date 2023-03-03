import warnings

from pint import UnitRegistry

##from pint_pandas import PintType

# The following warning is unnecessary:
#     "UnitStrippedWarning: The unit of the quantity is stripped when
#      downcasting to ndarray."

warnings.filterwarnings("ignore", message=".*unit of the quantity is strip.*")

ureg = UnitRegistry()
Q_ = ureg.Quantity

# PintType.ureg = ureg
# PintType.ureg.default_format = "~P"
