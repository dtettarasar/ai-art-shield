import pytest
import PIL
from PIL import Image, UnidentifiedImageError

from img_data import Img_Data

def test_init_class():

    img = Img_Data('test_files/cs50.jpg')
    assert img.img_path == 'test_files/cs50.jpg'

def test_load_image_file_errors():

    with pytest.raises(FileNotFoundError):
        Img_Data('test_files/wrong_file_name.jpg')

    with pytest.raises(UnidentifiedImageError):
        Img_Data("test_files/test_files.txt")

    