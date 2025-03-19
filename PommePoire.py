#Import dataset
import cv2
import numpy as np
import requests
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import sys
import datetime
from tensorflow import keras
from tensorflow.keras.models import Model
import tensorflow as tf
import pathlib
import os
import requests
import zipfile

# Télécharger le fichier ZIP depuis GitHub
data_dir = tf.keras.utils.get_file(
    "Apple.zip",
    "https://github.com/lucienrivat/PommePOire/raw/main/Apple.zip",
    extract=False
)

# Extraire le fichier ZIP dans /content/datasets
with zipfile.ZipFile(data_dir, 'r') as zip_ref:
    zip_ref.extractall('/content/datasets')

# Définir le chemin du dossier contenant les images
data_dir = pathlib.Path('/content/datasets/Apple')
print("Dossier des images :", data_dir)
print("Chemin absolu :", os.path.abspath(data_dir))

# Compter le nombre d'images dans le dataset
image_count = len(list(data_dir.glob('*/*')))
print("Nombre d'images trouvées :", image_count)
