import PIL
from PIL import Image, UnidentifiedImageError
import os
import sys
import logging
import argparse
import numpy as np

from img_data import Img_Data

def main():

    print("Hello from ai-art-shield!")

    parser = load_parser()

    args = parser.parse_args()

    # Logique principale du programme basée sur les arguments analysés
    if args.verbose:

        # Ici tu configurerais ton logging pour être plus verbeux
        logging.getLogger().setLevel(logging.DEBUG)
        logging.debug("Verbose mode enabled")

    logging.info(f"Command executed : {args.command}")

    if args.command == 'secure':

        logging.info(f"Image to protect : {args.input}")
        logging.info(f"Saved file path : {args.output}")
        logging.info(f"Strength protection : {args.strength}")

        img = Img_Data('test_img', args.verbose)
        

    elif args.command == 'verify':
        
        # Récupération des chemins des images depuis les arguments
        protected_input_path = args.protected_input
        original_input_path = args.original_input
        output_report_path = args.output_report

        # strict_mode = args.strict_mode # A Garder pour une future implémentation si besoin

        logging.info(f"Image protégée à vérifier : {protected_input_path}")
        logging.info(f"Image originale pour comparaison : {original_input_path}")



def load_parser():

    # argparse settings
    parser = argparse.ArgumentParser(
        description="AI Art Shield is a command-line tool developed in Python for protecting visual artworks from generative artificial intelligence systems. The project is part of Harvard's CS50P course.",
        formatter_class=argparse.RawTextHelpFormatter # Pour garder le formatage des descriptions multilignes
    )

    # Création des sous-commandes (secure, verify)
    subparsers = parser.add_subparsers(
        dest='command', 
        help='available commands', 
        required=True # Rend la sous-commande obligatoire
    )

    # --- Sous-commande 'secure' ---
    secure_parser = subparsers.add_parser(
        'secure', 
        help='Apply anti-IA protections to an image.',
        description="""
        This command applies a set of protection techniques
        (such as invisible DCT watermarking) to an image to protect it
        from AI model training and analysis.
        """
    )

    secure_parser.add_argument(
        '--input', 
        '-i', 
        type=str, 
        required=True, 
        help='Define the path for the input image file to protect (ex: image.jpg).'
    )

    secure_parser.add_argument(
        '--output', 
        '-o', 
        type=str, 
        required=True, 
        help='Define the path for the output image file to save (ex: image_protected.jpg).'
    )

    secure_parser.add_argument(
        '--strength', 
        '-s', 
        type=float, 
        default=5.0, # Valeur par défaut
        help='Protection strength (floating value, e.g. 1.0, 5.0, 10.0). The higher the value, the stronger and more visible the protection.'
    )

    secure_parser.add_argument(
        '--verbose',
        '-v',
        action='store_true', # stocke True si l'argument est présent
        help='Enables verbose mode for additional debugging information.'
    )

    # --- Sous-commande 'verify' (pour plus tard) ---
    verify_parser = subparsers.add_parser(
        'verify', 
        help='Checks whether an image has been protected and/or altered.',
        description="""
        This command analyzes an image to detect the presence of
        protections and verify its integrity via digital signatures or hashes.
        For this version, it compares a protected image against its original
        to measure the alteration level.
        """
    )
    verify_parser.add_argument(
        '--protected-input', # Nom plus explicite pour l'image protégée
        '-p',                # Raccourci pour 'protected'
        type=str,
        required=True,
        help='Path for the protected image file to verify (ex: image_protected.jpg).'
    )
    verify_parser.add_argument(
        '--original-input',  # Nouvel argument pour l'image originale
        '-o',                # Raccourci pour 'original'
        type=str,
        required=True,
        help='Path for the original, unprotected image file for comparison (ex: image_original.jpg).'
    )
    verify_parser.add_argument(
        '--output-report', # Pourrait générer un rapport
        '-r', 
        type=str, 
        help='path for the report file to save (optionnal).'
    )
    verify_parser.add_argument(
        '--verbose',
        '-v',
        action='store_true', # stocke True si l'argument est présent
        help='Enables verbose mode for additional debugging information.'
    )
    # Exemple d'autres arguments pour la vérification
    verify_parser.add_argument(
        '--strict-mode', 
        action='store_true', 
        help='Activates a strict verification mode to detect the slightest alteration.'
    )

    return parser



if __name__ == "__main__":
    main()
