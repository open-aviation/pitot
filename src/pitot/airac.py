from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pandas as pd

AIRAC_EPOCH = datetime(1998, 1, 29, tzinfo=timezone.utc)


def airac_cycle(
    timestamp: None | str | datetime = None,
    template: str = "{year:02d}{ordinal:02d}",
) -> str:
    """Returns the AIRAC cycle for the timestamp passed in parameter.

    >>> airac_cycle("2023-01-19")
    '2213'
    >>> airac_cycle("2023-01-26")
    '2301'
    >>> airac_cycle('2027-01-30')
    '2701'
    """
    if timestamp is None:
        timestamp = datetime.now(timezone.utc)

    DURATION_CYCLE = timedelta(days=28)

    ts = pd.to_datetime(timestamp, utc=True)
    delta = ts - AIRAC_EPOCH
    serial = delta.total_seconds() // DURATION_CYCLE.total_seconds()

    effective = AIRAC_EPOCH + serial * DURATION_CYCLE
    ordinal = (effective.timetuple().tm_yday - 1) // 28 + 1
    return template.format(year=effective.year % 100, ordinal=ordinal)


def airac_year_epoch(year: int) -> datetime:
    """Returns the effective date of the first AIRAC for the given year.

    >>> airac_year_epoch(2018)
    datetime.datetime(2018, 1, 4, 0, 0, tzinfo=datetime.timezone.utc)
    """
    beg = datetime(year, 1, 1, tzinfo=timezone.utc)
    extra_days = (beg - AIRAC_EPOCH).days % 28
    return beg - timedelta(days=extra_days - 28)


def airac_interval(airac: str) -> tuple[datetime, datetime]:
    """Returns the interval of dates for an (ICAO) AIRAC.

    >>> airac_interval("2403")
    (datetime.datetime(2024, 3, 21, ...), datetime.datetime(2024, 4, 18, ...))
    """
    # Validate airac format (4 digits)
    if not (len(airac) == 4 and airac.isdigit()):
        raise ValueError("AIRAC must be a 4-digit string.")

    # Extract cycle and validate
    cycle = int(airac[2:4])
    if not (1 <= cycle <= 14):
        raise ValueError("Cycle must be between 1 and 14.")

    # Extract year from airac and find the year epoch
    year = int(airac[:2])
    # Assuming year is 2000 + last two digits (adjust if your logic differs)
    full_year = 2000 + year
    y_epoch = airac_year_epoch(full_year)

    # Calculate the beginning and end of the AIRAC interval
    a_beg = y_epoch + timedelta(days=(cycle - 1) * 28)
    if airac_cycle(a_beg) != airac:
        raise ValueError(f"AIRAC mismatch for calculated start date: {a_beg}")

    a_end = a_beg + timedelta(days=28)

    # Return the interval
    return a_beg, a_end
