import base64
import errno

from app.Config import application
import os
import uuid


def image_upload(image_json, folder: str, required_filename=None) -> str:
    """
    uploads image to server, you must specify image file, folder name and (optionally) filename will generate
    filename + uuid4 (by default uuid4.hex + uuid4, this is made to prevent generating same names in case of
    simultaneous requests)
    :param image_json: dict with mime (image type) and data (base64)
    :param folder: str
    :param required_filename: str
    :return: str (path to file)
    """

    image_extention = image_json['mime'].split('/')[1]
    if required_filename is None:
        required_filename = str(uuid.uuid4().hex) + str(uuid.uuid4())
    image_name = str(required_filename) + '.' + image_extention

    with open(os.path.join(application.UPLOAD_FOLDER, folder, image_name), 'wb') as image:
        data = base64.b64decode(image_json['data'])
        image.write(data)
    path_to_save = 'images/' + folder + image_name
    return path_to_save


def image_remove(path):
    if path is None:
        return
    part_path = path.split('/')
    try:
        os.remove(application.UPLOAD_FOLDER + part_path[1] + '/' + part_path[2])
    except OSError as e:
        if e.errno != errno.ENOENT:
            raise
