from datetime import datetime
import pytz

IST = pytz.timezone("Asia/Kolkata")
UTC = pytz.utc


def ist_to_utc(dt_ist: datetime) -> datetime:
    if dt_ist.tzinfo is None:
        dt_ist = IST.localize(dt_ist)
    return dt_ist.astimezone(UTC)


def utc_to_ist(dt_utc: datetime) -> datetime:
    if dt_utc.tzinfo is None:
        dt_utc = UTC.localize(dt_utc)
    return dt_utc.astimezone(IST)
