import pytest

import PIL
from PIL import Image, UnidentifiedImageError
from PIL.JpegImagePlugin import JpegImageFile
from PIL.WebPImagePlugin import WebPImageFile

from img_data import Img_Data

def test_init_class():

    img_cs50 = Img_Data('test_files/cs50.jpg')
    
    assert img_cs50.img_path == 'test_files/cs50.jpg'

def test_load_image_file():

    img_cs50 = Img_Data('test_files/cs50.jpg')
    img_cookie = Img_Data("test_files/cookie_monster.webp")

    # Test la classe abstraite
    assert isinstance(img_cs50.img_file, Image.Image)
    assert isinstance(img_cookie.img_file, Image.Image)

    # Test la sous classe de la variable
    assert type(img_cs50.img_file) == JpegImageFile

    assert img_cs50.img_file.mode == "RGB"
    assert img_cs50.img_file.width == 2048
    assert img_cs50.img_file.height == 1366
    assert img_cs50.img_file.format == "JPEG"

    assert type(img_cookie.img_file) == WebPImageFile

    assert img_cookie.img_file.mode == "RGB"
    assert img_cookie.img_file.width == 1348
    assert img_cookie.img_file.height == 1600
    assert img_cookie.img_file.format == "WEBP"



def test_load_image_file_errors():

    with pytest.raises(FileNotFoundError):
        Img_Data('test_files/wrong_file_name.jpg')

    with pytest.raises(UnidentifiedImageError):
        Img_Data("test_files/test_files.txt")

