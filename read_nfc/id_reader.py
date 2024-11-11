"""

Okutulan kartlara ait ID ler txt dosyasına kaydedilir.
Bu ID ler tasks.json da kullanılmalıdır.

"""

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import time 

reader = SimpleMFRC522()

def add_unique_id(card_id):
    # card_ids.txt dosyasını aç ve mevcut ID'leri oku
    try:
        with open("card_ids.txt", "r") as file:
            existing_ids = file.read().splitlines()
    except FileNotFoundError:
        existing_ids = []  # Dosya yoksa boş listeyle başla

    # Eğer ID listede yoksa ekle
    if str(card_id) not in existing_ids:
        with open("card_ids.txt", "a") as file:
            file.write(f"{card_id}\n")
        print(f"Yeni kart ID'si kaydedildi: {card_id}")
    else:
        print(f"Kart ID'si zaten mevcut: {card_id}")

def read_card_id():
    try:
        while True:
            print("\nRFID kartınızı okutunuz...")
            id = reader.read()[0]
            print("Okunan RFID ID:", id)
            
            # Kart ID'sini ekle (eşsiz ise eklenir)
            add_unique_id(id)
            time.sleep(5)
    finally:
        GPIO.cleanup()

def main():
    read_card_id()

if __name__ == "__main__":
    main()
