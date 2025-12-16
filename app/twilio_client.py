import os
from twilio.rest import Client

# These will come from your .env file
TWILIO_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_FROM = os.getenv("TWILIO_WHATSAPP_FROM")   # e.g. "whatsapp:+14155238886"

twilio_client = Client(TWILIO_SID, TWILIO_TOKEN)

def send_whatsapp_message(to: str, body: str):
    """
    Sends a WhatsApp message via Twilio.
    `to` should be in format: "whatsapp:+91XXXXXXXXXX"
    """
    msg = twilio_client.messages.create(
        from_=TWILIO_FROM,
        to=to,
        body=body
    )
    return msg.sid
