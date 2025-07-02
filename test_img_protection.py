import pytest

import PIL
from PIL import Image, UnidentifiedImageError
from PIL.JpegImagePlugin import JpegImageFile
from PIL.WebPImagePlugin import WebPImageFile

import numpy as np

from img_data import Img_Data


# --- Fixtures pour Img_Data ---

@pytest.fixture
def img_cs50_instance():
    """Fournit une instance de Img_Data pour 'cs50.jpg'."""
    return Img_Data('test_files/cs50.jpg')

@pytest.fixture
def img_cookie_instance():
    """Fournit une instance de Img_Data pour 'cookie_monster.webp'."""
    return Img_Data("test_files/cookie_monster.webp")

def test_init_class(img_cs50_instance, img_cookie_instance):
    
    assert img_cs50_instance.img_path == 'test_files/cs50.jpg'
    assert img_cookie_instance.img_path == 'test_files/cookie_monster.webp'


# Test for load_file method------------------------------

def test_load_image_file(img_cs50_instance, img_cookie_instance):

    # Test la classe abstraite
    assert isinstance(img_cs50_instance.img_file, Image.Image)
    assert isinstance(img_cookie_instance.img_file, Image.Image)

    # Test la sous classe de la variable
    assert type(img_cs50_instance.img_file) == JpegImageFile

    assert img_cs50_instance.img_file.mode == "RGB"
    assert img_cs50_instance.img_file.width == 2048
    assert img_cs50_instance.img_file.height == 1366
    assert img_cs50_instance.img_file.format == "JPEG"

    assert type(img_cookie_instance.img_file) == WebPImageFile

    assert img_cookie_instance.img_file.mode == "RGB"
    assert img_cookie_instance.img_file.width == 1348
    assert img_cookie_instance.img_file.height == 1600
    assert img_cookie_instance.img_file.format == "WEBP"

def test_load_image_file_errors():

    with pytest.raises(FileNotFoundError):
        Img_Data('test_files/wrong_file_name.jpg')

    with pytest.raises(UnidentifiedImageError):
        Img_Data("test_files/test_files.txt")

def test_load_image_file_unexpected_io_error(mocker):
    # Simule une IOError lors de l'appel à Image.open
    # On patche Image.open car c'est la fonction externe qui pourrait lever cette erreur
    mocker.patch('PIL.Image.open', side_effect=IOError("Simulated unexpected I/O error"))

    # On a besoin d'un fichier existant pour que la première vérification (os.path.exists) passe
    # Mais Image.open va ensuite échouer
    dummy_existing_file = "test_files/cs50.jpg" # Ou n'importe quel fichier existant

    with pytest.raises(IOError) as excinfo:
        Img_Data(dummy_existing_file)

    # Tu peux aussi vérifier le message d'erreur si tu le souhaites
    assert "Simulated unexpected I/O error" in str(excinfo.value)
    assert "An unexpected error occurred while opening the image" in str(excinfo.value) # Vérifie le message de ta fonction


def test_load_image_file_other_unexpected_exception(mocker):
    # Simule une autre Exception inattendue lors de l'appel à Image.open
    mocker.patch('PIL.Image.open', side_effect=Exception("Something really bad happened!"))

    dummy_existing_file = "test_files/cs50.jpg"

    with pytest.raises(IOError) as excinfo: # Ton code convertit toutes les 'Exception' en 'IOError'
        Img_Data(dummy_existing_file)

    assert "Something really bad happened!" in str(excinfo.value)
    assert "An unexpected error occurred while opening the image" in str(excinfo.value)

# End of test for load_file method------------------------------

# Test for convert_pil_to_numpy method------------------------------

def test_pil_to_numpy(img_cs50_instance, img_cookie_instance):

    assert type(img_cs50_instance.numpy_array) == np.ndarray
    assert img_cs50_instance.numpy_array.ndim == 3 # Doit être un tableau 3D (hauteur, largeur, canaux)
    assert img_cs50_instance.numpy_array.shape[2] == 3 # Doit avoir 3 canaux (RGB)
    assert img_cs50_instance.numpy_array.dtype == np.uint8 # Doit être de type uint8 (0-255)

    assert type(img_cookie_instance.numpy_array) == np.ndarray
    assert img_cookie_instance.numpy_array.ndim == 3
    assert img_cookie_instance.numpy_array.shape[2] == 3
    assert img_cookie_instance.numpy_array.dtype == np.uint8
