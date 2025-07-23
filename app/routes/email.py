from fastapi import APIRouter
from app.schemas import EmailRequest
from app.email_utils import send_email

router = APIRouter()


@router.post("/send-email")
def send(email: EmailRequest):
    if send_email(email.email, email.message):
        return {"status": "sent"}
    return {"status": "failed"}
