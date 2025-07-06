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
    
    def _apply_dct_watermark_to_channel(self, channel_data, strength: float, seed_value):

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
    
    def apply_dct_watermark(self, input_np_array: np.ndarray, strength: float) -> np.ndarray: 

        """
        Applique un filigrane DCT à tous les canaux d'un tableau NumPy donné.
        Retourne un NOUVEAU tableau NumPy modifié.
        """

        logging.info(f"Applying DCT watermark with strength={strength}")

        # Travaille TOUJOURS sur une COPIE de l'entrée
        processed_image_np = input_np_array.copy()

         # --- GESTION DES IMAGES EN NIVEAUX DE GRIS ---
        if processed_image_np.ndim == 2: # Image en niveaux de gris (H, W)

            """
            Certaines bibliothèques ou formats d'image (comme certaines images PNG en niveaux de gris, 
            ou des tableaux NumPy créés directement) peuvent représenter une image en niveaux de gris sous la forme d'un tableau NumPy en deux dimensions ((hauteur, largeur)). 
            Il n'y a pas de troisième dimension pour les canaux. processed_image_np.ndim == 2 vérifie précisément si le tableau n'a que deux dimensions.
            """

            logging.warning("Input is a grayscale image. Converting to 3 channels (RGB) for DCT protection.")
            # Empile le canal gris sur 3 canaux pour simuler une image RGB
            processed_image_np = np.stack([processed_image_np, processed_image_np, processed_image_np], axis=-1)

            """
            np.stack() est une fonction NumPy qui empile des tableaux le long d'un nouvel axe.
            Nous lui passons une liste contenant le même tableau processed_image_np trois fois.
            axis=-1 signifie que le nouveau canal sera ajouté comme la dernière dimension.

            Le tableau (H, W) devient (H, W, 3). Chaque "canal" de cette nouvelle image RGB est une copie exacte du canal de niveaux de gris original. 
            Visuellement, l'image reste en niveaux de gris, mais elle est maintenant structurée comme une image couleur.
            """

        elif processed_image_np.ndim == 3 and processed_image_np.shape[2] == 1: # Image en niveaux de gris (H, W, 1)

            """
            D'autres bibliothèques (notamment Pillow après un convert('L') et pil_to_numpy, ou des formats spécifiques) peuvent représenter une image en niveaux de gris comme un tableau NumPy en trois dimensions,
            mais avec une seule valeur dans la troisième dimension ((hauteur, largeur, 1)).
            C'est techniquement une image "couleur" mais avec un seul canal.
            processed_image_np.ndim == 3 (trois dimensions) ET processed_image_np.shape[2] == 1 (la troisième dimension, celle des canaux, a une taille de 1).
            """

            logging.warning("Input is a 1-channel image. Converting to 3 channels (RGB) for DCT protection.")
            # Répète le canal unique sur 3 canaux
            processed_image_np = np.repeat(processed_image_np, 3, axis=2)

            """
            np.repeat() est utilisé pour répéter des éléments d'un tableau le long d'un axe donné.
            On repète le tableau processed_image_np (qui est (H, W, 1)) 3 fois le long de l'axis=2 (l'axe des canaux).
            Le tableau (H, W, 1) devient (H, W, 3). Encore une fois, chaque canal du nouvel "RGB" est une copie du canal de niveaux de gris original.
            """

        elif processed_image_np.ndim < 3 or processed_image_np.shape[2] < 3:
            # Ceci gère les images qui ne sont ni N&B ni RGB standard (ex: 2 canaux, ou autre)
            # Tu peux choisir de lever une erreur ici ou de simplement logguer et retourner

            """
            Ce dernier elif sert de garde-fou. Il attrape tous les autres cas d'images "non standard" qui ne sont ni des niveaux de gris simples (1 canal, qu'il soit 2D ou 3D) ni des images RGB/BGR classiques (3 canaux).
            Par exemple, cela pourrait être une image avec 2 canaux (alpha et un autre) ou 4 canaux (RGBA) qui n'est pas encore gérée.
            processed_image_np.ndim < 3 (moins de 3 dimensions, mais déjà géré par le premier if si c'est 2D), OU processed_image_np.shape[2] < 3 (3 dimensions, mais avec moins de 3 canaux, comme une image à 2 canaux).
            """

            logging.error("Input image must have at least 3 channels (RGB/BGR) for multi-channel DCT protection, or be a standard grayscale image.")
            raise ValueError("Unsupported image format: must be grayscale (1-channel) or RGB/BGR (3-channel).")
            
            """
            Nous levons une ValueError pour indiquer clairement que le format d'image d'entrée n'est pas supporté par l'algorithme de protection tel qu'il est conçu (qui nécessite 3 canaux pour la DCT multi-canal).
            C'est plus robuste que de simplement retourner la copie non modifiée, car cela force l'appelant à gérer un type d'entrée inattendu.
            """

        # --- ---

        # Itération sur les canaux (R, G, B)
        # range(3) pour les trois premiers canaux (0, 1, 2) correspondant à R, G, B dans Pillow.
        for i in range(3):
            channel_name = ["Red", "Green", "Blue"][i]
            logging.info(f"Processing channel: {channel_name}")
            
            # Génération d'une graine (seed) différente pour chaque canal
            # channel_seed = 42 + i: Permet de générer un filigrane aléatoire DIFFERENT pour chaque canal.
            # C'est une bonne pratique pour augmenter la robustesse et la complexité du filigrane.
            # L'utilisation de 42 est juste un nombre arbitraire "magique" souvent utilisé pour les graines.
            channel_seed = 42 + i

            # Extraction du canal et conversion en float
            # processed_image_np[:, :, i]: Sélectionne toutes les lignes, toutes les colonnes,
            # et le i-ème canal. Cela extrait un tableau 2D (le canal).
            # .astype(float): La DCT fonctionne mieux avec des nombres flottants, car les
            # coefficients peuvent être non entiers. On convertit explicitement le canal en float.
            processed_channel = self._apply_dct_watermark_to_channel(
                processed_image_np[:, :, i].astype(float),
                strength,
                channel_seed
            )
            
            # Réassignation du canal traité
            # Le canal modifié est remis à sa place dans le tableau d'image complet.
            processed_image_np[:, :, i] = processed_channel

        logging.info("DCT protection applied to all channels.")
        
        return processed_image_np
    
    # --- Méthode de Pipeline de Protection ---
    def secure_image(self, dct_strength: float = 0, wavelet_strength: float = 0, adversarial_strength: float = 0, qr_opacity: float = 0) -> np.ndarray:
        
        """
        Applique une combinaison de techniques de protection à l'image.
        Met à jour self.protected_numpy_array avec le résultat final.
        Retourne le tableau NumPy de l'image protégée.
        """
        logging.info("Starting image protection pipeline.")

        # Commencer avec une COPIE de l'array original
        # Cela garantit qu'on ne travaille JAMAIS directement sur self.numpy_array
        current_protected_image_np = self.numpy_array.copy()

        if dct_strength > 0:

            current_protected_image_np = self.apply_dct_watermark(current_protected_image_np, strength=dct_strength)
            logging.info("DCT watermark applied.")

        # Stocker le résultat final du pipeline dans l'attribut de la classe
        self.protected_numpy_array = current_protected_image_np

        logging.info("Image protection pipeline completed.")

    def export_protected_image(self, output_path: str, format: str = None, quality: int = -1):

        """
        Convertit le tableau NumPy protégé en image PIL et la sauvegarde.
        
        Args:
            output_path (str): Le chemin complet du fichier de sortie.
            format (str, optional): Le format de l'image (ex: "JPEG", "PNG"). Déduit par défaut de l'extension.
            quality (int, optional): Qualité pour les formats compressibles (0-100). -1 pour défaut.

        Raises:
            IOError: En cas d'erreur lors de la conversion ou de la sauvegarde de l'image.
            ValueError: Si protected_numpy_array n'est pas encore défini.
        """

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

    @property
    def protected_numpy_array(self):
        return self._protected_numpy_array
    
    @protected_numpy_array.setter
    def protected_numpy_array(self, value):
        self._protected_numpy_array = value
