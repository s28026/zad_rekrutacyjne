from .services.database import get_session
from .models.Message import Message
from celery import shared_task
from sqlalchemy.ext.asyncio import AsyncSession
import asyncio


@shared_task(ignore_result=False)
def add_message(form_data):
    errors = {}

    title = form_data["title"]
    message = form_data["content"]

    if not title:
        errors["title"] = "Title not provided"
    if not message:
        errors["message"] = "Message Content not provided"

    if not errors:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(_add_message_to_db(title, message))

    return {"errors": errors, "success": len(errors) == 0}


async def _add_message_to_db(title, message):
    async for session in get_session():
        await Message.add(session, title, message)
