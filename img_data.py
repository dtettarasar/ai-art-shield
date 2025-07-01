import logging
import os

import PIL
from PIL import Image, UnidentifiedImageError

class Img_Data:

    def __init__(self, img_path, debug_mode=False):
        
        self.img_path = img_path
        self.debug_mode = debug_mode

        self.load_file()
    
    def load_file(self):

        """
        Loads an image file using Pillow and performs initial checks.
        Returns a Pillow Image object, or throws an exception on error.
        """

        if self.debug_mode == True:

            logging.info("init load_file method from the img data class")
            logging.info(f"img file to load is located at: {self.img_path}")

        if not os.path.exists(self.img_path):

            raise FileNotFoundError(f"The input file '{self.img_path}' was not found.")
        
        try:

            img_pil = Image.open(self.img_path)

        except UnidentifiedImageError:

            # Cette exception est levée par Pillow si le fichier n'est pas une image valide
            raise UnidentifiedImageError(f"Unable to identify or open image file '{self.img_path}'. Check format or corruption.")

        except Exception as e:

            # Capture toute autre erreur inattendue lors de l'ouverture du fichier
            raise IOError(f"An unexpected error occurred while opening the image: {e}")


    @property
    def img_path(self):
        return self._img_path
    

    @img_path.setter
    def img_path(self, value):
        self._img_path = value

    @property
    def debug_mode(self):
        return self._debug_mode
    
    @debug_mode.setter
    def debug_mode(self, value):
        self._debug_mode = value

    @property
    def img_file(self):
        return self._img_file
    
    @img_file.setter
    def img_file(self):

        self._img_file = self.load_file()