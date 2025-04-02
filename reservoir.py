import serial
from PIL import Image
import os
import subprocess

ser = serial.Serial('COM3', 460800)  # Remplace 'COM3' par le port série de ton Arduino
ser.flushInput()

# Dimensions de l'image
width = 320
height = 240

num = 1
max_photos = 3  # Limite à 3 photos

while num <= max_photos:
    # Attendre le signal "READY"
    print("En attente du signal 'READY'...")
    while True:
        if ser.in_waiting > 0:
            try:
                line = ser.readline().decode('utf-8').strip()  # Lire une ligne et la décoder
                print(line)
                if line == "READY":
                    print("Signal 'READY' détecté. Début de la lecture des données...")
                    break
            except:
                pass

    # Lire les données de luminance
    frame_lum = []
    try:
        while len(frame_lum) < width * height:
            if ser.in_waiting > 0:
                data = ser.read()  # Lire un octet
                frame_lum.append(ord(data))  # Convertir en entier (0-255)
    except KeyboardInterrupt:
        print("Interruption par l'utilisateur.")

    # Attendre le signal "COULEUR"
    print("En attente du signal 'COULEUR'...")
    while True:
        try:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').strip()  # Lire une ligne et la décoder
                print(line)
                if line == "COULEUR":
                    print("Signal 'COULEUR' détecté. Début de la lecture des données...")
                    break
        except:
            pass

    # Lire les données de chromatique
    frame_col = []
    try:
        while len(frame_col) < width * height:
            if ser.in_waiting > 0:
                data = ser.read()  # Lire un octet
                frame_col.append(ord(data))  # Convertir en entier (0-255)
    except KeyboardInterrupt:
        print("Interruption par l'utilisateur.")

    print("Données reçues !")

    # Convertir les données en une image couleur
    index = 0
    dataCb = list()
    dataCr = list()
    bitmap = list()
    Alt = True

    for chroma in frame_col:
        if Alt:
            dataCr.extend([chroma,chroma])
            Alt = False
        else:
            dataCb.extend([chroma,chroma])
            Alt = True

    for y in range(height):
        for x in range(width):
            Y = frame_lum[index]
            Cb = dataCb[index]
            Cr = dataCr[index]

            R = int(max(0, min(255,Y + 1.40200 * (Cr - 0x80))))
            G = int(max(0, min(255,Y - 0.34414 * (Cb - 0x80) - 0.71414 * (Cr - 0x80))))
            B = int(max(0, min(255,Y + 1.77200 * (Cb - 0x80))))
            bitmap.append((R,G,B))
            index += 1

    # Sauvegarde de l'image
    image_filename = f"image_{num}.png"
    image_path = os.path.join(r"C:\Users\rivat\OneDrive\Documents\GitHub\PommePOire", image_filename)

    # Créer l'image en couleur avec Pillow
    img = Image.new('RGB', (width, height))
    img.putdata(bitmap)
    img.save(f"image_recue_couleur_{num}.png")
    print(f"Image enregistrée sous le nom 'image_recue_couleur_{num}.png'.")

    # Enregistrer l'image de chromatique
    img_col = Image.new('L', (width, height))
    img_col.putdata(frame_col)
    img_col.save(f"image_chromatique_{num}.png")
    print(f"Image de chromatique enregistrée sous le nom 'image_chromatique_{num}.png'.")

    # Enregistrer l'image de luminance
    img_lum = Image.new('L', (width, height))
    img_lum.putdata(frame_lum)
    img_lum.save(f"image_luminance_{num}.png")
    print(f"Image de luminance enregistrée sous le nom 'image_luminance_{num}.png'.")

    # Vérification si l'image a bien été enregistrée
    if os.path.exists(image_path):
        print(f"✅ Image enregistrée : {image_path}")
    else:
        print("❌ Problème : L'image n'a pas été sauvegardée.")

    # Envoi sur GitHub
    os.chdir(r"C:\Users\rivat\OneDrive\Documents\GitHub\PommePOire")

    # Vérifier si le dépôt Git est bien initialisé
    subprocess.run(["git", "status"], shell=True)

    subprocess.run(["git", "add", image_filename], shell=True)
    subprocess.run(["git", "commit", "-m", f"Ajout de l'image {num}"], shell=True)
    subprocess.run(["git", "push", "origin", "main"], shell=True)

    print(f"🚀 Image {num} envoyée sur GitHub !")

    num += 1

ser.close()
