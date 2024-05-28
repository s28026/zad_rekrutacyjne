from celery import shared_task


@shared_task(ignore_result=False)
def add_message(form_data):
    from .models import add_message

    errors = {}

    title = form_data["title"]
    message = form_data["content"]

    if not title:
        errors["title"] = "Title not provided"
    if not message:
        errors["message"] = "Message Content not provided"

    if not errors:
        add_message(title, message)

    return {"errors": errors, "success": len(errors) != 0}
