from images.process import save_image
from . import models


async def save_and_add_icon(image_file, user_id, db):
    """mock save image from UploadFile"""
    icon_path = await save_image(image_file, "./pics/users")

    user = db.query(models.User).filter(models.User.id == user_id).first()
    user.icon = icon_path
    db.commit()
