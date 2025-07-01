import pytest
from img_protection import Img_Protection

def test_init_class():

    img = Img_Protection('test_img.jpg')
    assert img.img_path == 'test_img.jpg'
