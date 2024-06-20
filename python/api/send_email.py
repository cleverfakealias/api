import logging
import os
import re
from http import HTTPStatus
import json
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


logger = logging.getLogger(__name__)

# Fetch the SendGrid API key once and store it in a variable
SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')

# Regular expression for simple email validation
EMAIL_REGEX = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'


def is_valid_email(email):
    return re.match(EMAIL_REGEX, email)


def send_email(name, email, message):
    # Validate the email address
    if not is_valid_email(email):
        return {'status': 'error', 'message': 'Invalid email address'}, HTTPStatus.BAD_REQUEST

    message = Mail(
        from_email='no_reply@benhickman.dev',
        to_emails='me@benhickman.dev',
        subject=f'New Email from {email} (BenHickman.dev)',
        plain_text_content=f'Name: {name}\nEmail: {email}\nMessage: {message}'
    )
    logger.info(f"Sending email: {message}")
    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        if response.status_code != 202:
            logger.error(f"Failed to send email, status code: {response.status_code}")
            return {'status': 'error', 'message': 'Failed to send email'}, HTTPStatus.INTERNAL_SERVER_ERROR
        return {'status': 'success'}, HTTPStatus.OK
    except Exception as e:
        # Log the actual error message
        logger.error(f"Error occurred: {str(e)}")
        return {'status': 'error', 'message': 'Failed to send email'}, HTTPStatus.INTERNAL_SERVER_ERROR


# async def handler(req, res):
#     # Read the request body as a string
#     body = await req.text()

#     # Parse the JSON from the string
#     data = json.loads(body)

#     name = data.get('name')
#     email = data.get('email')
#     message = data.get('message')

#     response = send_email(name, email, message)

#     return response


# send_email("ben", "me@benhickman.dev", "hello")
