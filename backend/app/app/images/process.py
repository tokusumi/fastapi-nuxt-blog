import os
from PIL import Image
from io import BytesIO
import hashlib
from datetime import datetime
from fastapi import UploadFile
from app.settings.configs import (
    AWS_BUCKET_NAME,
    S3_URL,
    aws_session
)


def hash_string(string: str) -> str:
    return hashlib.sha256(string.encode()).hexdigest()


def hash_image_filename(image_filename: str, parent_path: str) -> str:
    now = datetime.now().strftime("%Y/%m/%d")
    base, ext = image_filename.rsplit('.', 1)
    filename = hash_string(base) + '.' + ext
    filename = '/'.join([parent_path, now, filename])
    return filename


async def mock_save_image(image_file: UploadFile, path: str):
    """mock save image from UploadFile"""
    content = await image_file.read()
    stream = BytesIO(content)
    img = Image.open(stream)
    out_path = os.path.join(path, image_file.filename)
    img.save(out_path)
    return out_path


async def save_image(image_file: UploadFile, path: str):
    """save image from UploadFile into S3"""
    s3 = aws_session.resource('s3')
    filename = hash_image_filename(image_file.filename, path)
    s3.Bucket(AWS_BUCKET_NAME).put_object(Key=filename, Body=image_file.file)
    return S3_URL + filename
