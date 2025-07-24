from fastapi import APIRouter, HTTPException
from app.schemas import EmailRequest
from app.email_utils import send_email

router = APIRouter()


@router.post("/send-email")
def send(email: EmailRequest):
    # Here we can add any additional validation for the email or message if necessary
    try:
        # Call the email sending function
        if send_email(email.email, email.message):
            return {"status": "sent"}
        else:
            # If the email couldn't be sent, raise an exception with a meaningful message
            raise HTTPException(status_code=400, detail="Failed to send email")

    except Exception as e:
        # Catch unexpected errors and raise them as HTTP exceptions with a 500 status code
        raise HTTPException(
            status_code=500, detail=f"Internal Server Error: {str(e)}")
