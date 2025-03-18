import serial
import time
from PIL import Image
import numpy as np

def preprocess_image(image_path):
    img = Image.open(image_path).convert('L').resize((32, 32))  # Adapter la taille selon le CNN
    img_array = np.array(img) / 255.0  # Normalisation
    return img_array.flatten().tolist()

def send_image_to_arduino(image_path, port="COM3", baudrate=115200):
    ser = serial.Serial(port, baudrate, timeout=1)
    time.sleep(2)  # Laisser le temps à l'Arduino de se réinitialiser
    
    img_data = preprocess_image(image_path)
    img_str = ','.join(map(str, img_data))
    
    ser.write((img_str + "\n").encode())
    
    response = ser.readline().decode().strip()
    ser.close()
    
    if response == "pomme":
        print("Diode verte allumée (pomme reconnue)")
    elif response == "poire":
        print("Diode jaune allumée (poire reconnue)")
    else:
        print("Erreur de reconnaissance")

# Exemple d'utilisation
if __name__ == "__main__":
    send_image_to_arduino("chemin/vers/image.jpg")
