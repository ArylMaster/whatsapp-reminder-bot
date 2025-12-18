from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()


class Reminder(Base):
    __tablename__ = "reminders"

    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    run_at_utc = Column(DateTime, nullable=False)
    created_at_utc = Column(DateTime, default=datetime.utcnow)


class ReminderEvent(Base):
    __tablename__ = "reminder_events"

    id = Column(Integer, primary_key=True, index=True)
    reminder_id = Column(Integer, nullable=True)
    phone_number = Column(String, nullable=False)
    event_type = Column(String, nullable=False)
    event_time_utc = Column(DateTime, default=datetime.utcnow)
    details = Column(Text, nullable=True)
