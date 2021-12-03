# -*- coding: utf-8 -*-
"""Application configuration."""
from version import __version__
import os

# FastAPI logging level
DEBUG = True
# FastAPI project name
PROJECT_NAME = "SulfurTechEduAuth"
VERSION = __version__
# Path to config file
BASEDIR = os.path.abspath(os.path.dirname(__file__))
# Secret Key
SECRET_KEY = os.urandom(32)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
UPLOAD_FOLDER = BASEDIR + '/../static/'
CLOUDINARY_URL = 'cloudinary://585514832173685:ZEND6qDYgV-H6rQEJRp931vS-dw@hqndlzoag'