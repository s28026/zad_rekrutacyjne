from celery.result import AsyncResult
from fastapi import APIRouter, Depends, Request

from ..services.database import get_session


router = APIRouter()


@router.get("/check/{task_id}")
async def read_task(task_id):
    res = AsyncResult(task_id)
    return {"status": res.status, "result": res.result}


@router.post("/form")
async def submit_form(req: Request, session=Depends(get_session)):
    from ..tasks import add_message

    form = await req.form()
    form_data = {key: value for key, value in form.items()}
    task = add_message.delay(form_data)
    return {"task_id": task.id}
