# WhatsApp Reminder Bot

A FastAPI-based WhatsApp reminder automation system that uses Twilio Webhooks to receive messages, parses user instructions, stores reminders in a database, and schedules outgoing WhatsApp notifications using APScheduler.

This project supports:
- Receiving WhatsApp messages via Twilio Sandbox
- Parsing commands in the format: `remind:ISO_TIMESTAMP|Message`
- Storing reminders in SQLite using SQLAlchemy ORM
- Scheduling reminders with APScheduler
- Sending WhatsApp reminders via Twilio API
- Fully local development using ngrok tunneling

---

## 📂 Project Structure

```
app/
 ├── main.py            # FastAPI app + webhook logic
 ├── db.py              # Database engine + session factory
 ├── models.py          # Reminder ORM model
 ├── scheduler.py       # Scheduling + reminder sender
 └── twilio_client.py   # Twilio WhatsApp message sender

.env                    # Environment variables (NOT committed)
requirements.txt        # Python dependencies
.gitignore              # Ignored and sensitive files
README.md               # Project documentation
```

---

## ▶️ Running the Project

### 1. Create a virtual environment
```bash
python -m venv .venv
.\.venv\Scripts\activate
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up `.env`
Create a `.env` file in the project root:

```
TWILIO_ACCOUNT_SID=your_sid_here
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_WHATSAPP_FROM=whatsapp:+14155238886
```

### 4. Start FastAPI server
```bash
uvicorn app.main:app --reload
```

### 5. Start ngrok (to expose your local server)
```bash
ngrok http 8000
```

Set your Twilio Sandbox webhook (in the console) to:
```
https://<your-ngrok-url>/twilio/webhook
```

---

## 📬 Example Message (send on WhatsApp)
```
remind:2025-12-14T22:26|Test reminder from phone
```

---

## 📌 Notes
- Twilio Sandbox only sends/receives messages from numbers joined to the sandbox.
- SQLite DB files should NOT be committed to Git.
- `.env` contains credentials — never commit it.
- This is a development setup; production deployment will replace ngrok with a permanent domain.

