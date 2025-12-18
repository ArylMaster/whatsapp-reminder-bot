from fastapi import APIRouter, Depends, Form
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import AsyncSessionLocal
from app.logging.logger import get_logger
from app.logging.events import log_event
from app.services.reminders import create_reminder, ReminderError
from app.nlp.parser import parse_reminder
from app.commands import handle_list, handle_cancel


router = APIRouter()
logger = get_logger("webhook")


async def get_db():
    async with AsyncSessionLocal() as db:
        yield db


@router.post("/twilio/webhook")
async def twilio_webhook(
    Body: str = Form(...),
    From: str = Form(...),
    db: AsyncSession = Depends(get_db),
):
    phone_number = From
    text = Body.strip()

    logger.info(f"Message received from {phone_number}: {text}")

    await log_event(
        db,
        phone_number=phone_number,
        event_type="RECEIVED",
        details=text,
    )

    # ---- Command handling ----
    lowered = text.lower()

    if lowered == "list":
        return await handle_list(
            db=db,
            phone_number=phone_number,
        )

    if lowered.startswith("cancel"):
        parts = lowered.split()
        if len(parts) != 2 or not parts[1].isdigit():
            return "❌ Usage: cancel <reminder_id>"

        return await handle_cancel(
            db=db,
            phone_number=phone_number,
            reminder_id=int(parts[1]),
        )


    # ---- NLP parsing ----
    message, run_at_ist = parse_reminder(text)
    print("DEBUG webhook message:", repr(message))
    print("DEBUG webhook run_at_ist:", run_at_ist)


    if not run_at_ist:
        await log_event(
            db,
            phone_number=phone_number,
            event_type="PARSE_FAILED",
            details=text,
        )
        return (
            "❌ Sorry, I couldn't understand that.\n"
            "Try something like:\n"
            "• remind me to drink water in 10 minutes\n"
            "• call mom tomorrow at 7"
        )

    # ---- Create reminder ----
    try:
        confirmation = await create_reminder(
            db=db,
            phone_number=phone_number,
            message=message,
            run_at_ist=run_at_ist,
        )
        return confirmation

    except ReminderError as e:
        await log_event(
            db,
            phone_number=phone_number,
            event_type="VALIDATION_FAILED",
            details=str(e),
        )
        return f"❌ {str(e)}"

    except Exception as e:
        logger.exception("Unexpected error")
        await log_event(
            db,
            phone_number=phone_number,
            event_type="ERROR",
            details=str(e),
        )
        return "❌ Something went wrong. Please try again later."
