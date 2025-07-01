import pytest

import PIL
from PIL import Image, UnidentifiedImageError
from PIL.JpegImagePlugin import JpegImageFile

from img_data import Img_Data

def test_init_class():

    img_cs50 = Img_Data('test_files/cs50.jpg')
    
    assert img_cs50.img_path == 'test_files/cs50.jpg'

def test_load_image_file():

    img_cs50 = Img_Data('test_files/cs50.jpg')

    # Test la classe abstraite
    assert isinstance(img_cs50.img_file, Image.Image)

    # Test la sous classe de la variable
    assert type(img_cs50.img_file) == JpegImageFile

    assert img_cs50.img_file.mode == "RGB"
    assert img_cs50.img_file.width == 2048
    assert img_cs50.img_file.height == 1366
    assert img_cs50.img_file.format == "JPEG"

def test_load_image_file_errors():

    with pytest.raises(FileNotFoundError):
        Img_Data('test_files/wrong_file_name.jpg')

    with pytest.raises(UnidentifiedImageError):
        Img_Data("test_files/test_files.txt")

