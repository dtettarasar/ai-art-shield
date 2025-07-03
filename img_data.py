import logging
import os

import PIL
from PIL import Image, UnidentifiedImageError
import numpy as np

from scipy.fftpack import dct, idct

class Img_Data:

    def __init__(self, img_path):
        
        self.img_path = img_path

        self.load_file()
        self.convert_pil_to_numpy()

        logging.debug("finish to load file in img data class")
        logging.debug("img file: ")
        logging.debug(self.img_file)
    
    def load_file(self):

        """
        Loads an image file using Pillow and performs initial checks.
        Returns a Pillow Image object, or throws an exception on error.
        """

        logging.info("init load_file method from the img data class")
        logging.info(f"img file to load is located at: {self.img_path}")

        if not os.path.exists(self.img_path):

            raise FileNotFoundError(f"The input file '{self.img_path}' was not found.")
        
        try:

            img_pil = Image.open(self.img_path)
            
            logging.info(f"Image loaded: '{self.img_path}', Format: {img_pil.format}, Mode: {img_pil.mode}")
            # --- Débogage de l'objet PIL.Image ---
            logging.debug("--- Attributs de l'objet PIL.Image.Image ---")
            logging.debug(f"Image Mode: {img_pil.mode}")
            logging.debug(f"Image Size (width, height): {img_pil.size}")
            logging.debug(f"Image Width: {img_pil.width}")
            logging.debug(f"Image Height: {img_pil.height}")
            logging.debug(f"Image Format: {img_pil.format}")
            logging.debug(f"Image Bands: {img_pil.getbands()}")

            if img_pil.info:
                logging.debug(f"Image Info (metadata): {img_pil.info}")
            else:
                logging.debug("No specific metadata found in img_pil.info.")

            # Convertir l'image en RGB si nécessaire pour assurer 3 canaux pour le traitement DCT
            if img_pil.mode != 'RGB':
                logging.debug(f"Converting image from {img_pil.mode} to RGB mode.")
                img_pil = img_pil.convert('RGB')
            
            self.img_file = img_pil


        except UnidentifiedImageError:

            # Cette exception est levée par Pillow si le fichier n'est pas une image valide
            raise UnidentifiedImageError(f"Unable to identify or open image file '{self.img_path}'. Check format or corruption.")

        except Exception as e:

            # Capture toute autre erreur inattendue lors de l'ouverture du fichier
            raise IOError(f"An unexpected error occurred while opening the image: {e}")
    
    # ces deux fonctions servent à convertir un fichier image en array numpy et vice versa. Cette conversion de la donnée est nécessaire pour appliquer les protections.
    def convert_pil_to_numpy(self):

        """Convertit un objet PIL Image en un tableau NumPy."""
        # S'assurer que l'image est en RGB avant la conversion pour cohérence
        if self.img_file.mode != "RGB":
            self.img_file = self.img_file.convert('RGB')
    
        self.numpy_array = np.array(self.img_file)
        logging.debug("Image converted from PIL to NumPy array and stored in self.numpy_array.")
    
    def convert_numpy_to_pil(self, numpy_array: np.ndarray) -> Image.Image:
        
        """
        Convertit un tableau NumPy donné en un objet PIL Image.
        Cette méthode ne modifie pas l'état interne de l'objet Img_Data.
        
        Args:
            numpy_array (np.ndarray): Le tableau NumPy à convertir.
                                      Il doit être de type np.uint8 avec 2 ou 3 dimensions.

        Returns:
            PIL.Image.Image: L'objet PIL Image résultant de la conversion.
        
        Raises:
            TypeError: Si l'entrée n'est pas un tableau NumPy.
            ValueError: Si le tableau NumPy n'est pas dans un format attendu.
        """

        logging.info("Attempting to convert NumPy array to PIL Image.")

        if not isinstance(numpy_array, np.ndarray):
            raise TypeError("Input must be a NumPy array.")
        
        # S'assurer que le type de données est correct pour PIL (généralement np.uint8)
        # S'il n'est pas uint8, le convertir.
        if numpy_array.dtype != np.uint8:
            logging.warning(f"NumPy array has dtype {numpy_array.dtype}, converting to np.uint8.")
            numpy_array = numpy_array.astype(np.uint8)

        # Pillow peut déduire le mode (RGB, L, etc.) de la forme du tableau
        # Par exemple: (H, W) -> 'L', (H, W, 3) -> 'RGB', (H, W, 4) -> 'RGBA'
        try:
            pil_image = Image.fromarray(numpy_array)
            logging.info(f"NumPy array converted to PIL Image. Mode: {pil_image.mode}, Size: {pil_image.size}")
            return pil_image
        except Exception as e:
            # Capturer les erreurs potentielles de Image.fromarray (ex: forme inattendue)
            raise ValueError(f"Failed to convert NumPy array to PIL Image: {e}")
    
    def _apply_dct_watermark_to_channel(self, channel_data, strength, seed_value):

        """
        Prend un seul canal de couleur (par exemple, le canal Rouge) sous forme de tableau NumPy 2D et y applique le filigrane.
        """

        logging.debug(f"Starting channel processing (shape: {channel_data.shape})")

        # 1. Centrage des données des pixels
        # Les valeurs de pixels sont généralement entre 0 et 255.
        # Pour que la DCT fonctionne mieux (et pour des raisons mathématiques de symétrie),
        # il est courant de centrer les données autour de zéro.
        # On soustrait 128 (qui est environ la moitié de 255).
        
        centered_channel = channel_data - 128.0
        logging.debug(f"Centered channel. Min: {np.min(centered_channel)}, Max: {np.max(centered_channel)}")

        # 2. Application de la Transformation Cosinus Discrète (DCT)
        # scipy.fftpack.dct effectue la DCT.
        # Pour une image 2D (qui est ce qu'est un canal), la DCT doit être appliquée deux fois:
        # d'abord sur les lignes, puis sur les colonnes (ou vice-versa).
        # .T (transpose) est utilisé pour appliquer la DCT le long des colonnes après l'avoir appliquée le long des lignes.
        # 'norm='ortho'' assure une transformation orthogonale, ce qui signifie que l'IDCT est simplement l'inverse de la DCT.
        dct_coeffs = dct(dct(centered_channel.T, norm='ortho').T, norm='ortho')
        logging.debug(f"DCT applied. Coeffs[0,0]: {dct_coeffs[0,0]:.2f}")

        # 3. Génération du Filigrane (Watermark)
        # np.random.seed(seed_value): Fixe la graine du générateur de nombres aléatoires.
        # C'est CRUCIAL. Si tu appliques le filigrane à nouveau (par exemple, pour la vérification),
        # tu auras besoin de générer EXACTEMENT le même bruit aléatoire. La seed garantit cela.
        # watermark = np.random.normal(0, 2, channel_data.shape): Génère un tableau de bruit
        # aléatoire qui suit une distribution normale (gaussienne) avec une moyenne de 0 et
        # un écart-type de 2. La taille du tableau est la même que celle du canal d'image.
        # Ce bruit sera notre "signature" ou "protection" ajoutée.
        np.random.seed(seed_value)
        watermark = np.random.normal(0, 2, channel_data.shape)
        logging.debug(f"Watermark generated. Min: {np.min(watermark):.2f}, Max: {np.max(watermark):.2f}")

        # 4. Injection du Filigrane dans les Coefficients DCT
        # C'est l'étape clé du filigranage. Nous ajoutons le bruit généré aux coefficients DCT.
        # La 'strength' est un facteur de mise à l'échelle. Plus la force est élevée,
        # plus le filigrane est prononcé (plus visible, mais aussi plus résistant).
        dct_coeffs += strength * watermark
        logging.debug(f"Watermark added to DCT coefficients. New Coeffs[0,0]: {dct_coeffs[0,0]:.2f}")

        # 5. Application de la Transformation Cosinus Discrète Inverse (IDCT)
        # Nous utilisons idct pour revenir du domaine fréquentiel au domaine spatial (pixels).
        # C'est l'inverse exact de l'étape 2.
        reconstructed_centered_channel = idct(idct(dct_coeffs.T, norm='ortho').T, norm='ortho')
        logging.debug(f"IDCT applied.")

        # 6. Dé-centrage et Limitation des valeurs des pixels
        # Nous ajoutons 128.0 pour ramener les valeurs à la plage 0-255.
        # np.clip(..., 0, 255): Les transformations peuvent parfois produire des valeurs
        # en dehors de la plage valide [0, 255]. `np.clip` assure que toutes les valeurs
        # restent dans cette plage en les "coupant" si elles sont trop basses (<0) ou trop hautes (>255).
        # .astype(np.uint8): Convertit le tableau en type entier non signé de 8 bits,
        # ce qui est le format standard pour les pixels d'image (0-255).
        watermarked_channel = np.clip(reconstructed_centered_channel + 128.0, 0, 255).astype(np.uint8)
        logging.debug(f"Processed and clipped channel. Min: {np.min(watermarked_channel)}, Max: {np.max(watermarked_channel)}")
    
        return watermarked_channel


    @property
    def img_path(self):
        return self._img_path
    

    @img_path.setter
    def img_path(self, value):
        self._img_path = value

    @property
    def img_file(self):
        return self._img_file
    
    @img_file.setter
    def img_file(self, value):

        self._img_file = value

    @property
    def numpy_array(self):
        return self._numpy_array

    @numpy_array.setter
    def numpy_array(self, value):
        self._numpy_array = value
