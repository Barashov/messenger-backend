from starlette.datastructures import UploadFile
import uuid
import os


async def save_image(image: UploadFile, folder: str) -> str:
    """
    save image in media folder
    :param image: image object from form
    :param folder: image save folder in media
    :return: image path
    """
    folder_path = f'media/{folder}/'
    filename = folder_path + str(uuid.uuid4()) + '.' + image.filename

    with open(filename, 'wb') as f:
        f.write(await image.read())

    return filename

