from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from fastapi import HTTPException
from typing import Dict, Any
import os
from starlette.responses import JSONResponse


async def send_email(request: Any, response: Any) -> JSONResponse:
    data = await request.json()
    name: str = data.get('name')
    email: str = data.get('email')
    message: str = data.get('message')

    email_message = Mail(
        from_email='web@benhickman.dev',  # Replace with your SendGrid email
        to_emails=email,
        subject='Contact Form Message',
        plain_text_content=f'Message from {name} ({email}): {message}'
    )

    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(email_message)
        if 200 <= response.status_code < 300:
            return JSONResponse(status_code=200, content={"message": "Thank you"})
        else:
            raise HTTPException(
                status_code=500,
                detail={'status': 'error', 'message': 'Email sending failed'}
            )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={'status': 'error', 'message': str(e)}
        )
