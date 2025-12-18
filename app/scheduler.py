from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from app.db import AsyncSessionLocal
from app.models import Reminder
from app.logging.events import log_event
from app.services.twilio_sender import TwilioSender
from app.services.retries import retry_async

scheduler = AsyncIOScheduler()
sender = TwilioSender()

def start_scheduler():
    if not scheduler.running:
        scheduler.start()


def schedule_reminder(reminder: Reminder):
    scheduler.add_job(
        execute_reminder,
        "date",
        run_date=reminder.run_at_utc,
        args=[reminder.id],
        id=str(reminder.id),
        replace_existing=True,
    )


async def execute_reminder(reminder_id: int):
    """
    Runs when reminder time is reached.
    """
    async with AsyncSessionLocal() as db:
        reminder = await db.get(Reminder, reminder_id)
        if not reminder:
            return  # already cancelled or cleaned up

        # ---- Log execution start ----
        await log_event(
            db,
            phone_number=reminder.phone_number,
            reminder_id=reminder.id,
            event_type="EXECUTION_STARTED",
        )

        async def send_message():
            await sender.send(
                to=reminder.phone_number,
                body=f"⏰ Reminder:\n{reminder.message}",
            )

        try:
            await retry_async(send_message)

            await log_event(
                db,
                phone_number=reminder.phone_number,
                reminder_id=reminder.id,
                event_type="SENT",
            )

        except Exception as e:
            await log_event(
                db,
                phone_number=reminder.phone_number,
                reminder_id=reminder.id,
                event_type="SEND_FAILED",
                details=str(e),
            )


        # ---- Cleanup ----
        await db.delete(reminder)
        await db.commit()

        await log_event(
            db,
            phone_number=reminder.phone_number,
            reminder_id=reminder.id,
            event_type="CLEANED_UP",
        )
