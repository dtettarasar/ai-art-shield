class Img_Protection:

    def __init__(self, img_path, debug_mode=False):
        
        self.img_path = img_path
        self.debug_mode = debug_mode

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
