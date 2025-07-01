import pytest
from img_protection import Img_Protection

def test_init_class():

    img = Img_Protection('test_img.jpg')
    assert img.img_path == 'test_img.jpg'
    assert img.debug_mode == False

    img_debug = Img_Protection('test_img_debug.jpg', True)
    assert img_debug.img_path == 'test_img_debug.jpg'
    assert img_debug.debug_mode == True