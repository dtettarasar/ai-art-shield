import pytest
from img_data import Img_Data

def test_init_class():

    img = Img_Data('test_files/cs50.jpg')
    assert img.img_path == 'test_files/cs50.jpg'
    assert img.debug_mode == False

    img_debug = Img_Data('test_files/cs50.jpg', True)
    assert img_debug.img_path == 'test_files/cs50.jpg'
    assert img_debug.debug_mode == True

def test_load_image_file_errors():

    with pytest.raises(FileNotFoundError):
        Img_Data('test_files/wrong_file_name.jpg')