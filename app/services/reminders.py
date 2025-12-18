from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Reminder
from app.scheduler import schedule_reminder
from app.logging.events import log_event
from app.nlp.timezone import ist_to_utc


class ReminderError(Exception):
    pass


async def create_reminder(
    *,
    db: AsyncSession,
    phone_number: str,
    message: str,
    run_at_ist: datetime,
) -> str:
    """
    Creates, stores, schedules a reminder.
    Returns confirmation message text.
    Raises ReminderError on failure.
    """

    # ---- Validation ----
    if run_at_ist <= datetime.now():
        raise ReminderError("Time is in the past")

    if not message.strip():
        raise ReminderError("Empty reminder message")

    # ---- Timezone conversion ----
    run_at_utc = ist_to_utc(run_at_ist)

    # ---- Persist reminder ----
    reminder = Reminder(
        phone_number=phone_number,
        message=message,
        run_at_utc=run_at_utc,
    )

    db.add(reminder)
    await db.commit()
    await db.refresh(reminder)

    # ---- Audit logs ----
    await log_event(
        db,
        phone_number=phone_number,
        reminder_id=reminder.id,
        event_type="CREATED",
        details=f"run_at_utc={run_at_utc.isoformat()}",
    )

    # ---- Schedule job ----
    schedule_reminder(reminder)

    await log_event(
        db,
        phone_number=phone_number,
        reminder_id=reminder.id,
        event_type="SCHEDULED",
    )

    # ---- Confirmation text ----
    confirmation = (
        "✅ Reminder set\n"
        f"🕒 {run_at_ist.strftime('%d %b %Y, %I:%M %p')} IST\n"
        f"📝 {message}"
    )

    return confirmation
