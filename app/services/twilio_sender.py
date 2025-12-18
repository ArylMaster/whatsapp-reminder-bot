from twilio.rest import Client
from app.config import (
    TWILIO_ACCOUNT_SID,
    TWILIO_AUTH_TOKEN,
    TWILIO_WHATSAPP_FROM,
)


class TwilioSender:
    def __init__(self):
        self.client = Client(
            TWILIO_ACCOUNT_SID,
            TWILIO_AUTH_TOKEN,
        )

    async def send(self, *, to: str, body: str):
        # Twilio client is sync; wrap call
        self.client.messages.create(
            from_=TWILIO_WHATSAPP_FROM,
            to=to,
            body=body,
        )
