from fastapi import (
    File,
    FastAPI,
    Response,
    UploadFile,
)

from fastapi.responses import JSONResponse

from PIL import Image

import pytesseract as ptsr

import io


api = FastAPI()

IMG_URL = '/analyze_image'


@api.post(IMG_URL)
async def analyze_doc(image: UploadFile = File(...)):
    try:
        image_bytes = await image.read()
        img = Image.open(
            io.BytesIO(
                image_bytes
            )
        )
        text = ptsr.image_to_string(img)
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
