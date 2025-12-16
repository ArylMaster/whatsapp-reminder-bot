import os
from fastapi import FastAPI, BackgroundTasks, Form
from pydantic import BaseModel
import datetime
import sqlalchemy as sa
from dotenv import load_dotenv

# load .env automatically
load_dotenv()

from .db import engine, Base, AsyncSessionLocal
from .models import Reminder
from .scheduler import start_scheduler, schedule_job_for
from .twilio_client import send_whatsapp_message

app = FastAPI()

class TwilioWebhookPayload(BaseModel):
    From: str
    Body: str

@app.on_event("startup")
async def on_startup():
    # Create DB tables if not exist
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    # start the scheduler
    start_scheduler()
    # reschedule pending reminders
    async with AsyncSessionLocal() as session:
        result = await session.execute(sa.select(Reminder).where(Reminder.sent == False))
        reminders = result.scalars().all()
        now = datetime.datetime.utcnow()
        for r in reminders:
            # only schedule future reminders
            if r.when and r.when > now:
                schedule_job_for(r.id, r.when)

@app.get("/")
def home():
    return {"message": "WhatsApp Reminder Bot is running!"}

@app.post("/twilio/webhook")
async def twilio_webhook(
    From: str = Form(...),
    Body: str = Form(...)
):
    text = Body.strip()
    phone = From.strip()

    if not text.lower().startswith("remind:"):
        return {"status": "ignored", "detail": "Send as remind:ISO|message"}

    try:
        rest = text[len("remind:"):].strip()
        time_part, message = rest.split("|", 1)
        when = datetime.datetime.fromisoformat(time_part)
    except Exception as e:
        return {"status": "error", "detail": f"Failed to parse message: {e}"}

    async with AsyncSessionLocal() as session:
        reminder = Reminder(phone=phone, message=message.strip(), when=when)
        session.add(reminder)
        await session.commit()
        await session.refresh(reminder)

        schedule_job_for(reminder.id, reminder.when)

    return {"status": "ok", "id": reminder.id}