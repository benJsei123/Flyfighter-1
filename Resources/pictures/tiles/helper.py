import os
from PIL import Image


def resize_and_rename_images(directory, new_size=(448, 448)):
    for i, filename in enumerate(os.listdir(directory), start=1):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):  # Überprüfe die Dateierweiterung
            try:
                # Öffne das Bild
                with Image.open(os.path.join(directory, filename)) as img:
                    # Ändere die Größe des Bilds
                    img = img.resize(new_size, Image.LANCZOS)
                    
                    # Neuen Dateinamen festlegen
                    new_filename = f"tile_pic_{i}.png"
                    
                    # Speichere das umgewandelte Bild als PNG
                    img.save(os.path.join(directory, new_filename), 'PNG')
                    
                    # Rückmeldung in der Konsole
                    print(f"{filename} umgewandelt zu {new_filename}")

            except Exception as e:
                print(f"Ein Fehler ist aufgetreten bei der Datei {filename}: {e}")

# Pfad zum Verzeichnis 'tiles', relativ zum aktuellen Arbeitsverzeichnis
# Wenn das Skript direkt im Verzeichnis 'tiles' ausgeführt wird, dann kann der Pfad einfach '.' sein.
directory_path = '.'
resize_and_rename_images(directory_path)
