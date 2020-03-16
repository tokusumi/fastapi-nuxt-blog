import os
from PIL import Image
from io import BytesIO
from fastapi import UploadFile


async def save_image(image_file: UploadFile, path: str):
    """mock save image from UploadFile"""
    content = await image_file.read()
    stream = BytesIO(content)
    img = Image.open(stream)
    out_path = os.path.join(path, image_file.filename)
    img.save(out_path)
    return out_path
