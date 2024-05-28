from typing import Annotated
from celery.utils.serialization import jsonify
from fastapi import APIRouter, Depends, Form, Request
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.templating import Jinja2Templates

from ..tasks import add_message
from ..models.Message import Message

from ..services.database import get_session


router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/")
def index(req: Request):
    return templates.TemplateResponse("index.html", {"request": req})


@router.get("/form")
def read_form(req: Request):
    return templates.TemplateResponse(
        "form.html", {"request": req, "errors": {}, "success": False}
    )


@router.post("/form")
async def form(
    req: Request,
    session: AsyncSession = Depends(get_session),
):
    errors = {}

    form = await req.form()
    title: str = form.get("title")
    content: str = form.get("content")

    if not title:
        errors["title"] = "Title is required"
    if not content:
        errors["message"] = "Content is required"

    if not errors:
        await Message.add(session, title, content)

    print(errors)
    return templates.TemplateResponse(
        "form.html", {"request": req, "errors": errors, "success": len(errors) == 0}
    )


@router.get("/async-form")
def async_form(req: Request):
    return templates.TemplateResponse(
        "async_form.html",
        {"request": req, "errors": {}, "success": True},
    )


@router.get("/messages")
async def messages(req: Request, session: AsyncSession = Depends(get_session)):
    messages = await Message.all(session)

    return templates.TemplateResponse(
        "messages.html",
        {"request": req, "messages": messages},
    )


@router.get("/about")
async def about(req: Request):
    return templates.TemplateResponse("about.html", {"request": req})
