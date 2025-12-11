from fastapi import (
    File,
    FastAPI,
    Response,
    UploadFile,
)

from fastapi.responses import JSONResponse

from fastapi.middleware.cors import CORSMiddleware

from celery import shared_task
from email.mime.text import MIMEText

from PIL import Image

import pytesseract as ptsr

import aiosmtplib

import io


api = FastAPI()

api.add_middleware(
    CORSMiddleware,
    allow_origins=[
        '127.0.0.1', 
        'localhost'
    ],
    allow_credentials=True,
    allow_methods=['*']
)

IMG_URL = '/analyze_image'


EMAIL = 'spaminhaler123@gmail.com'

PASSWORD = '123456'


@shared_task
async def send_email(subject: str, message: str, to_email: str):
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = EMAIL
    msg['To'] = to_email
    
    await aiosmtplib.send(
        msg, hostname='smtp.example.com', port=587, 
        username=EMAIL,
        password=PASSWORD,
        use_tls=True
    )


@api.post('/send_message_to_email/')
async def send_message_to_email(email: str, text: str):
    subject = 'Image has been analyzed'
    message = '%s. Text: %s' % (subject, text)
    send_email.delay(subject, message, email)

    return JSONResponse(
        content={'message': '%s' % subject},
        status_code=200
    )


@api.post(IMG_URL)
async def analyze_doc(image: UploadFile = File(...), email: str = EMAIL):
    try:
        image_bytes = await image.read()
        img = Image.open(
            io.BytesIO(
                image_bytes
            )
        )
        text = ptsr.image_to_string(img)
        await send_message_to_email(email=email, text=text)
        return JSONResponse(
            content={
                'text': text,
            },
            status_code=200,
        )
    except Exception as e:
        return JSONResponse(
            content={
                'text': str(e),
            },
            status_code=418,
        )


@api.exception_handler(404)
async def not_found_exception_handler(request, exc):
    return JSONResponse(status_code=404, content={'detail': 'Not found!'})


@api.exception_handler(422)
async def unprocessable_entity_exception_handler(request, exc):
    return JSONResponse(status_code=422, content={'detail': 'Unprocessable entity!'})


@api.exception_handler(Exception)
async def generic_exception_handler(request, exc):
    return JSONResponse(status_code=200, content={'detail': str(exc)})
