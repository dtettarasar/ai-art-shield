import logging
import os

import PIL
from PIL import Image, UnidentifiedImageError

class Img_Data:

    def __init__(self, img_path):
        
        self.img_path = img_path

        self.img_file = self.load_file()

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
            
            return img_pil


        except UnidentifiedImageError:

            # Cette exception est levée par Pillow si le fichier n'est pas une image valide
            raise UnidentifiedImageError(f"Unable to identify or open image file '{self.img_path}'. Check format or corruption.")

        except Exception as e:

            # Capture toute autre erreur inattendue lors de l'ouverture du fichier
            raise IOError(f"An unexpected error occurred while opening the image: {e}")
    
    # ces deux fonctions servent à convertir un fichier image en array numpy et vice versa. Cette conversion de la donnée est nécessaire pour appliquer les protections.
    def convert_pil_to_numpy(self):
        """"""
    
    def convert_numpy_to_pil(self):
        """"""

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