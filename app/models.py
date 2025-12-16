from sqlalchemy import Column, Integer, String, DateTime, Boolean
from .db import Base
import datetime

class Reminder(Base):
    __tablename__ = "reminders"

    id = Column(Integer, primary_key=True, index=True)
    phone = Column(String, index=True)      # e.g. "whatsapp:+91..."
    message = Column(String)
    when = Column(DateTime)                 # UTC datetime when to send
    sent = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
