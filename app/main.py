from fastapi import FastAPI

from app.webhook import router as webhook_router
from app.startup import load_pending_reminders
from app.health import router as health_router


app = FastAPI()

app.include_router(webhook_router)
app.include_router(health_router)


@app.on_event("startup")
async def startup_event():
    await load_pending_reminders()
