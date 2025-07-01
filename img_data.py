import logging
import os
class Img_Data:

    def __init__(self, img_path, debug_mode=False):
        
        self.img_path = img_path
        self.debug_mode = debug_mode

        self.load_file()
    
    def load_file(self):

        if self.debug_mode == True:

            logging.info("init load_file method from the img data class")
            logging.info(f"img file to load is located at: {self.img_path}")

        return None

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