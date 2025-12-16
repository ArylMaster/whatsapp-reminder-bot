import asyncio
from datetime import datetime
import sqlalchemy as sa

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.date import DateTrigger

from .db import AsyncSessionLocal
from .models import Reminder
from .twilio_client import send_whatsapp_message

scheduler = AsyncIOScheduler()

async def send_reminder(reminder_id: int):
    """
    This async function is called by APScheduler at the scheduled time.
    It fetches the reminder from the DB, sends the WhatsApp message (via Twilio),
    marks it sent, and commits the change.
    """
    async with AsyncSessionLocal() as session:
        result = await session.execute(sa.select(Reminder).where(Reminder.id == reminder_id))
        reminder = result.scalar_one_or_none()
        if not reminder or reminder.sent:
            return

        # Twilio client is synchronous, so run it in a thread to avoid blocking the event loop
        body = reminder.message
        to = reminder.phone

        try:
            await asyncio.to_thread(send_whatsapp_message, to, body)
            reminder.sent = True
            session.add(reminder)
            await session.commit()
        except Exception as e:
            # For now, just print — we'll add logging/ retry later.
            print(f"Failed to send reminder {reminder_id}: {e}")

def schedule_job_for(reminder_id: int, when: datetime):
    """
    Schedule a one-shot job to run at `when` that will call send_reminder(reminder_id).
    The job id is the reminder's id converted to str so we can refer to it later.
    """
    job_id = str(reminder_id)
    # Avoid duplicate job ids: remove existing if present
    try:
        existing = scheduler.get_job(job_id)
        if existing:
            existing.remove()
    except Exception:
        pass

    trigger = DateTrigger(run_date=when)
    scheduler.add_job(send_reminder, trigger, args=[reminder_id], id=job_id)

def start_scheduler():
    """
    Start the APScheduler. Call this once during application startup.
    """
    if not scheduler.running:
        scheduler.start()
