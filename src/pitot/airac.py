from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pandas as pd


def airac_cycle(
    timestamp: None | str | datetime = None,
    template: str = "{year:02d}{ordinal:02d}",
) -> str:
    """Returns the AIRAC cycle for the timestamp passed in parameter.

    >>> airac_cycle("2023-01-19")
    '2213'
    >>> airac_cycle("2023-01-26")
    '2301'
    """
    if timestamp is None:
        timestamp = datetime.now(timezone.utc)

    DURATION_CYCLE = timedelta(days=28)
    EPOCH = datetime(1901, 1, 10, tzinfo=timezone.utc)

    ts = pd.to_datetime(timestamp, utc=True)
    delta = ts - EPOCH
    serial = delta.total_seconds() // DURATION_CYCLE.total_seconds()

    effective = EPOCH + serial * DURATION_CYCLE
    ordinal = (effective.timetuple().tm_yday - 1) // 28 + 1
    return template.format(year=effective.year % 100, ordinal=ordinal)
