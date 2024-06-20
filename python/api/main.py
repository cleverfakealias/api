import logging
from fastapi import FastAPI, HTTPException, Request
from typing import Dict, Any
from starlette.responses import JSONResponse
from .send_email import send_email

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(message)s')
logger = logging.getLogger(__name__)

app = FastAPI()

@app.post("/send_email")
async def send_email_endpoint(request: Request) -> JSONResponse:
    try:
        # Log the incoming request
        request_data = await request.json()
        logger.info(f"Received request: {request_data}")

        # Process the request and send the email
        response = send_email(
            request_data.get('name'), 
            request_data.get('email'), 
            request_data.get('message')
            )
        
        # Log the response
        logger.info(f"Response: {response}")

        return response
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={'status': 'error', 'message': str(e)}
        )