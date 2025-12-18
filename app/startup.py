from datetime import datetime

from app.db import AsyncSessionLocal, engine
from app.models import Base, Reminder
from app.scheduler import start_scheduler, schedule_reminder
from app.logging.logger import get_logger

logger = get_logger("startup")


async def init_db():
    """
    Create tables if they don't exist.
    Safe to run multiple times.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def load_pending_reminders():
    """
    Reload all future reminders from DB and schedule them.
    Runs once on app startup.
    """
    logger.info("Initializing database")
    await init_db()

    logger.info("Starting scheduler rehydration")
    start_scheduler()

    async with AsyncSessionLocal() as db:
        result = await db.execute(
            Reminder.__table__.select().where(
                Reminder.run_at_utc > datetime.utcnow()
            )
        )
        reminders = result.fetchall()

        for row in reminders:
            reminder = row[0]
            schedule_reminder(reminder)
            logger.info(
                f"Re-scheduled reminder {reminder.id} "
                f"for {reminder.run_at_utc.isoformat()}"
            )

    logger.info("Scheduler rehydration complete")
