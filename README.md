# WhatsApp Reminder Bot

A FastAPI-based WhatsApp reminder automation system that uses Twilio webhooks to receive messages, parses user instructions, stores reminders in a database, and schedules messages to be sent at the right time using APScheduler.

This project supports:
- Receiving WhatsApp messages via Twilio Sandbox
- Parsing commands in the format: `remind:ISO_TIMESTAMP|Message`
- Storing reminders in SQLite using SQLAlchemy ORM
- Scheduling reminders with APScheduler
- Sending WhatsApp reminders back to the user using Twilio API

## 🚀 Features
- Webhook endpoint for Twilio
- Database-backed reminder storage
- Scheduled job execution
- Working end-to-end WhatsApp reminder system
- Fully local development with ngrok tunneling

## 🛠 Tech Stack
- **FastAPI** – Web framework for the webhook endpoint
- **SQLAlchemy + SQLite** – ORM and database
- **APScheduler** – Scheduler for sending reminders
- **Twilio API** – WhatsApp messaging
- **ngrok** – Tunneling for local development

## 📂 Project Structure
app/
├── main.py # FastAPI app + webhook logic
├── db.py # Database engine + session
├── models.py # Reminder ORM model
├── scheduler.py # Scheduling + reminder sender
└── twilio_client.py # Twilio WhatsApp message sender
.env # Environment variables (NOT committed)
requirements.txt # Python dependencies
.gitignore # Ignored files

## ▶️ Running the Project

1. **Create a virtual environment**
python -m venv .venv
..venv\Scripts\activate

2. **Install dependencies**
pip install -r requirements.txt

3. **Set up `.env`**
TWILIO_ACCOUNT_SID=...
TWILIO_AUTH_TOKEN=...
TWILIO_WHATSAPP_FROM=whatsapp:+14155238886

4. **Start FastAPI server**
uvicorn app.main:app --reload

5. **Start ngrok**
ngrok http 8000

6. **Set Twilio Sandbox webhook to**
https://<ngrok-url>/twilio/webhook

## 📬 Example Message
Send this to your Twilio Sandbox WhatsApp:
remind:2025-12-14T22:26|Test reminder from phone


## 📌 Notes
- Twilio Sandbox only sends and receives messages from numbers that joined the sandbox.
- SQLite DB is local; do not commit `.db` files.
- `.env` contains secrets and must be kept out of Git.

---

More features (NLP parsing, list/cancel commands, deployment) will be added next.