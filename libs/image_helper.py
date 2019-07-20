import os
import re
from typing import Union
from werkzeug.datastructures import FileStorage

from flask_uploads import UploadSet, IMAGES

IMAGE_SET = UploadSet("images", IMAGES) ## set of allowed extensions

def save_image(image: FileStorage, folder: str=None, name: str=None):
    """Takes FileStoreg and save it"""
    pass


def get_path():
    """Returns image file path"""
    pass


def find_image_any_format():
    """Takes a filename an returns image of any of the accepted formats"""
    pass


def _retrieve_filename():
    """Takes FileStorage and return file name"""
    pass

def is_filename_safe():
    """Regex check if string matches"""
    pass


def get_basename():
    """Returns full image file name"""
    pass


def get_extension():
    """Returns file extension"""
    pass