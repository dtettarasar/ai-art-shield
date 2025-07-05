import logging
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

# End of test for convert_pil_to_numpy method------------------------------

# Test for convert_numpy_to_pil method------------------------------

def test_numpy_to_pil(img_cs50_instance, img_cookie_instance):

    # Appel de la méthode convert_numpy_to_pil sur l'instance,
    # en lui passant le numpy_array de cette même instance.
    img_cs50_from_numpy = img_cs50_instance.convert_numpy_to_pil(img_cs50_instance.numpy_array)
    img_cookie_from_numpy = img_cookie_instance.convert_numpy_to_pil(img_cookie_instance.numpy_array)

    assert isinstance(img_cs50_from_numpy, Image.Image)
    assert img_cs50_from_numpy.mode == "RGB"
    assert img_cs50_from_numpy.width == img_cs50_instance.img_file.width
    assert img_cs50_from_numpy.height == img_cs50_instance.img_file.height

    assert isinstance(img_cookie_from_numpy, Image.Image)
    assert img_cookie_from_numpy.mode == "RGB"
    assert img_cookie_from_numpy.width == img_cookie_instance.img_file.width
    assert img_cookie_from_numpy.height == img_cookie_instance.img_file.height

    # Vérifier si les valeurs des pixels sont les mêmes après l'aller-retour
    # Convertir les deux en float pour la comparaison.
    reconverted_np_cs50 = np.array(img_cs50_from_numpy)
    assert np.allclose(img_cs50_instance.numpy_array.astype(float), reconverted_np_cs50.astype(float), atol=1)

    reconverted_np_cookie = np.array(img_cookie_from_numpy)
    assert np.allclose(img_cookie_instance.numpy_array.astype(float), reconverted_np_cookie.astype(float), atol=1)


# End of test for convert_numpy_to_pil method------------------------------

# Test _apply_dct_watermark_to_channel()------------------------------

def test_dct_watermark_output_properties(img_cs50_instance):

    """
    Vérifie les propriétés de base du canal après application du filigrane DCT.
    """

    # Accède au tableau NumPy depuis l'instance
    img_np = img_cs50_instance.numpy_array

    # Récupère le canal rouge (index 0) et le convertit en float
    # Comme la méthode _apply_dct_watermark_to_channel soustrait 128.0
    # et travaille souvent avec des floats pour les transformées.
    channel_data = img_np[:, :, 0].astype(float)
    strength = 5.0
    seed = 42

    watermarked_channel = img_cs50_instance._apply_dct_watermark_to_channel(channel_data.copy(), strength, seed)

    # 1. Vérifier le type de données
    assert watermarked_channel.dtype == np.uint8

    # 2. Vérifier les dimensions
    assert watermarked_channel.shape == channel_data.shape

    # 3. Vérifier que les valeurs de pixels sont dans la plage [0, 255]
    assert np.min(watermarked_channel) >= 0
    assert np.max(watermarked_channel) <= 255


def test_dct_watermark_introduces_change(img_cs50_instance):
    
    """
    Vérifie qu'un filigrane avec strength > 0 introduit bien une modification.
    """

    # Accède au tableau NumPy depuis l'instance
    img_np = img_cs50_instance.numpy_array

    original_channel = img_np[:, :, 0].astype(float)
    strength = 5.0 # Une force non nulle
    seed = 42

    watermarked_channel = img_cs50_instance._apply_dct_watermark_to_channel(
        original_channel.copy(), strength, seed
    )

    # Convertir l'original en uint8 pour une comparaison plus directe si allclose échoue
    # Ou comparer les deux en float si tu veux être très précis sur l'algorithme lui-même
    # avant le np.clip et astype(uint8) final.
    # Pour le test final de la fonction, on compare les uint8 résultants.
    
    # Il DOIT y avoir une différence significative
    # np.array_equal est strict, allclose est tolérant.
    # On s'attend à ce que ce ne soit PAS égal
    assert not np.array_equal(original_channel.astype(np.uint8), watermarked_channel)

    # Vérifier une différence moyenne perceptible
    # La différence absolue moyenne entre les pixels originaux et watermarked doit être > un certain seuil
    mean_diff = np.mean(np.abs(original_channel - watermarked_channel.astype(float)))
    # Le seuil (ici 0.5) est à ajuster en fonction de ta strength et de ce qui est "perceptible"
    assert mean_diff > 0.5 # Avec strength=5, la différence devrait être notable


def test_dct_watermark_no_change_with_zero_strength(img_cs50_instance):
    """
    Vérifie qu'un filigrane avec strength = 0 n'introduit pratiquement aucun changement.
    """

    # Accède au tableau NumPy depuis l'instance
    img_np = img_cs50_instance.numpy_array

    original_channel = img_np[:, :, 0].astype(float)
    strength = 0.0 # Force nulle
    seed = 42

    watermarked_channel = img_cs50_instance._apply_dct_watermark_to_channel(
        original_channel.copy(), strength, seed
    )
    
    # Il devrait y avoir des différences MINIMES dues aux conversions float/uint8 et arrondis
    # np.allclose est parfait ici pour gérer ces petites tolérances
    assert np.allclose(original_channel.astype(np.uint8), watermarked_channel, atol=1)
    # atol=1 signifie une tolérance absolue d'une unité sur les valeurs de pixel (0-255).
    # Cela couvre les arrondis légers qui peuvent survenir.


def test_dct_watermark_reproducibility(img_cs50_instance):
    """
    Vérifie que le filigrane est reproductible avec la même graine et la même force.
    """

    # Accède au tableau NumPy depuis l'instance
    img_np = img_cs50_instance.numpy_array

    original_channel = img_np[:, :, 0].astype(float)
    strength = 7.0
    seed = 123

    watermarked_channel_1 = img_cs50_instance._apply_dct_watermark_to_channel(
        original_channel.copy(), strength, seed
    )
    watermarked_channel_2 = img_cs50_instance._apply_dct_watermark_to_channel(
        original_channel.copy(), strength, seed # Même force et même graine
    )

    # Les deux résultats doivent être identiques pixel par pixel
    assert np.array_equal(watermarked_channel_1, watermarked_channel_2)


def test_dct_watermark_different_seed_different_result(img_cs50_instance):
    
    """
    Vérifie que des graines différentes produisent des résultats différents.
    """

    # Accède au tableau NumPy depuis l'instance
    img_np = img_cs50_instance.numpy_array

    original_channel = img_np[:, :, 0].astype(float)
    strength = 7.0
    seed1 = 123
    seed2 = 456 # Graine différente

    watermarked_channel_1 = img_cs50_instance._apply_dct_watermark_to_channel(
        original_channel.copy(), strength, seed1
    )
    watermarked_channel_2 = img_cs50_instance._apply_dct_watermark_to_channel(
        original_channel.copy(), strength, seed2
    )

    # Les deux résultats ne devraient PAS être identiques (sauf cas rarissimes de coïncidence de bruit)
    assert not np.array_equal(watermarked_channel_1, watermarked_channel_2)


def test_dct_watermark_strength_scaling(img_cs50_instance):
    """
    Vérifie que l'augmentation de la force augmente l'ampleur du changement.
    """

    # Accède au tableau NumPy depuis l'instance
    img_np = img_cs50_instance.numpy_array

    original_channel = img_np[:, :, 0].astype(float) # Garder en float pour plus de précision

    seed = 42

    # Force faible
    watermarked_low_strength = img_cs50_instance._apply_dct_watermark_to_channel(
        original_channel.copy(), strength=1.0, seed_value=seed
    )
    diff_low = np.mean(np.abs(original_channel - watermarked_low_strength.astype(float)))

    # Force élevée
    watermarked_high_strength = img_cs50_instance._apply_dct_watermark_to_channel(
        original_channel.copy(), strength=10.0, seed_value=seed
    )
    diff_high = np.mean(np.abs(original_channel - watermarked_high_strength.astype(float)))

    # La différence avec une force élevée doit être significativement plus grande
    assert diff_high > diff_low * 2 # Par exemple, au moins deux fois plus grande, à ajuster

# End of test _apply_dct_watermark_to_channel()------------------------------

# Test apply_dct_watermark()------------------------------

@pytest.fixture
def sample_grayscale_image_np():
    """Fixture qui fournit une image NumPy en niveaux de gris simple pour les tests."""
    # Une image 3x3 en niveaux de gris
    return np.full((3, 3), 100, dtype=np.uint8)

@pytest.fixture
def sample_grayscale_image_np_1_channel():
    """Fixture qui fournit une image NumPy en niveaux de gris avec 1 canal explicite (H, W, 1)."""
    # Une image 3x3 avec un canal explicite
    return np.full((3, 3, 1), 100, dtype=np.uint8)

def test_apply_dct_watermark_returns_numpy_array(img_cs50_instance, img_cookie_instance):

    """Vérifie que la fonction retourne bien un tableau NumPy."""

    # Accède au tableau NumPy depuis l'instance
    img_np_cs50 = img_cs50_instance.numpy_array
    img_np_cookie = img_cookie_instance.numpy_array

    protected_img_np_cs50 = img_cs50_instance.apply_dct_watermark(img_np_cs50, strength=5.0)
    protected_img_np_cookie = img_cookie_instance.apply_dct_watermark(img_np_cookie, strength=5.0)

    assert isinstance(protected_img_np_cs50, np.ndarray)
    assert isinstance(protected_img_np_cookie, np.ndarray)

def test_apply_dct_watermark_returns_same_shape(img_cs50_instance, img_cookie_instance):

    """Vérifie que l'image traitée a les mêmes dimensions que l'originale."""

    # Accède au tableau NumPy depuis l'instance
    img_np_cs50 = img_cs50_instance.numpy_array
    img_np_cookie = img_cookie_instance.numpy_array

    original_shape_cs50 = img_np_cs50.shape
    protected_img_np_cs50 = img_cs50_instance.apply_dct_watermark(img_np_cs50, strength=5.0)

    original_shape_cookie = img_np_cookie.shape
    protected_img_np_cookie = img_cookie_instance.apply_dct_watermark(img_np_cookie, strength=5.0)

    assert protected_img_np_cs50.shape == original_shape_cs50
    assert protected_img_np_cookie.shape == original_shape_cookie

def test_apply_dct_watermark_modifies_image(img_cs50_instance, img_cookie_instance):

    """Vérifie que la protection modifie réellement les pixels de l'image."""

    # Accède au tableau NumPy depuis l'instance
    img_np_cs50 = img_cs50_instance.numpy_array
    img_np_cookie = img_cookie_instance.numpy_array
    
    protected_img_np_cs50 = img_cs50_instance.apply_dct_watermark(img_np_cs50, strength=5.0)
    protected_img_np_cookie = img_cookie_instance.apply_dct_watermark(img_np_cookie, strength=5.0)
    
    # Assure-toi qu'au moins un pixel est différent
    assert not np.array_equal(img_np_cs50, protected_img_np_cs50)
    assert not np.array_equal(img_np_cookie, protected_img_np_cookie)

    # Vérifie que les valeurs des pixels restent dans une plage raisonnable (0-255)
    assert np.all(protected_img_np_cs50 >= 0) and np.all(protected_img_np_cs50 <= 255)
    assert np.all(protected_img_np_cookie >= 0) and np.all(protected_img_np_cookie <= 255)


def test_apply_dct_watermark_converts_and_modifies_grayscale_2d_image(sample_grayscale_image_np, img_cookie_instance, caplog):

    # Vérifie que la fonction convertit une image 2D niveaux de gris en 3 canaux et lui applique la protection.

    # Accède au tableau NumPy depuis l'instance
    img_grayscale_np = sample_grayscale_image_np

    caplog.set_level(logging.WARNING) # Attendre un WARNING pour la conversion

    initial_shape = img_grayscale_np.shape # (H, W)
    
    protected_img_np = img_cookie_instance.apply_dct_watermark(img_grayscale_np, strength=5.0)
    
    # 1. Vérifie que le message d'avertissement de conversion a été loggé
    assert "Input is a grayscale image. Converting to 3 channels (RGB) for DCT protection." in caplog.text
    
    # 2. Vérifie que l'image de sortie est maintenant en 3 canaux
    assert protected_img_np.shape == (initial_shape[0], initial_shape[1], 3)
    
    # 3. Vérifie que l'image a bien été modifiée (elle n'est plus identique à l'originale si traitée)
    # Pour cela, il faut 're-convertir' l'originale en 3 canaux pour la comparaison ou faire une vérif sur un canal
    # Ici, je compare avec l'originale empilée en 3 canaux.
    original_3_channels = np.stack([img_grayscale_np, img_grayscale_np, img_grayscale_np], axis=-1)
    assert not np.array_equal(original_3_channels, protected_img_np)
    
    # 4. Vérifie que les valeurs de pixels restent dans la plage 0-255
    assert np.all(protected_img_np >= 0) and np.all(protected_img_np <= 255)

def test_apply_dct_watermark_unsupported_channel_count(img_cookie_instance):
    """
    Vérifie que la fonction lève une ValueError pour des images avec un nombre
    de canaux non supporté (ex: 2 ou 4 canaux sans être une RGBA standard reconnue).
    """
    # Créer une image NumPy avec 2 canaux (exemple de format non supporté par la logique actuelle)
    # Imaginons une image (Hauteur, Largeur, 2)
    unsupported_2_channel_image = np.full((10, 10, 2), 100, dtype=np.uint8)

    # Créer une image NumPy avec 4 canaux, mais on assume que ta fonction
    # ne la traite pas comme une RGBA si la logique pour RGBA n'est pas encore implémentée.
    # Si tu décides de supporter RGBA plus tard, ce test devra être modifié.
    # Pour l'instant, on la traite comme un "cas non supporté" si non explicitement gérée.
    unsupported_4_channel_image = np.full((10, 10, 4), 100, dtype=np.uint8)


    # Test pour 2 canaux
    with pytest.raises(ValueError, match="^Unsupported image format: must be grayscale \\(1-channel\\) or RGB/BGR \\(3-channel\\).$"):
        img_cookie_instance.apply_dct_watermark(unsupported_2_channel_image, strength=5.0)

    # Test pour 4 canaux (si non géré comme RGBA spécifique)
    # Note : Si plus tard tu adaptes ta fonction pour traiter 4 canaux (RGBA),
    # ce test devra être ajusté ou supprimé pour ce cas.
    # with pytest.raises(ValueError, match="^Unsupported image format: must be grayscale \\(1-channel\\) or RGB/BGR \\(3-channel\\).$"):
        #apply_dct_protection(unsupported_4_channel_image, strength=5.0)

def test_apply_dct_watermark_converts_and_modifies_grayscale_1_channel_image(sample_grayscale_image_np_1_channel, caplog):
    """
    Vérifie que la fonction convertit une image 1-canal niveaux de gris en 3 canaux et lui applique la protection.
    """

# End of test apply_dct_watermark()------------------------------
