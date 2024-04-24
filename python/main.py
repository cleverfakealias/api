from fastapi import FastAPI, HTTPException
from typing import Dict, Any
from send_email import send_email

app = FastAPI()

@app.post("/send_email")
async def send_email_endpoint(request: Dict[str, Any]) -> Dict[str, str]:
    try:
        return await send_email(request, None)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={'status': 'error', 'message': str(e)}
        )
