from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import ReminderEvent


async def log_event(
    db: AsyncSession,
    *,
    phone_number: str,
    event_type: str,
    reminder_id: int | None = None,
    details: str | None = None,
):
    event = ReminderEvent(
        reminder_id=reminder_id,
        phone_number=phone_number,
        event_type=event_type,
        event_time_utc=datetime.utcnow(),
        details=details,
    )

    db.add(event)
    await db.commit()
