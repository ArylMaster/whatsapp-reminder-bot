from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models import Reminder
from app.scheduler import scheduler
from app.logging.events import log_event


async def handle_list(
    *,
    db: AsyncSession,
    phone_number: str,
) -> str:
    result = await db.execute(
        select(Reminder).where(Reminder.phone_number == phone_number)
    )
    reminders = result.scalars().all()

    if not reminders:
        return "📭 You have no upcoming reminders."

    lines = ["📋 Your reminders:"]
    for r in reminders:
        lines.append(
            f"{r.id}. {r.message} — "
            f"{r.run_at_utc.strftime('%d %b %Y, %I:%M %p')} UTC"
        )

    return "\n".join(lines)


async def handle_cancel(
    *,
    db: AsyncSession,
    phone_number: str,
    reminder_id: int,
) -> str:
    reminder = await db.get(Reminder, reminder_id)

    if not reminder or reminder.phone_number != phone_number:
        return "❌ Reminder not found."

    # Remove from scheduler if present
    try:
        scheduler.remove_job(str(reminder.id))
    except Exception:
        pass  # job may not exist

    await db.delete(reminder)
    await db.commit()

    await log_event(
        db,
        phone_number=phone_number,
        reminder_id=reminder_id,
        event_type="CANCELLED",
    )

    return f"🗑️ Reminder {reminder_id} cancelled."
