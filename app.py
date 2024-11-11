from flask import Flask, render_template, jsonify, redirect, url_for
import json
import time
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import threading
from queue import Queue

app = Flask(__name__)

# Global değişkenler
last_task_queue = Queue()  # Thread-safe iletişim için kuyruk kullanımı
current_task = None

# JSON dosyasından görevleri yükleme
def load_tasks():
    try:
        with open("./static/tasks.json", "r", encoding='utf-8') as file:
            tasks = json.load(file)["tasks"]
        print("Görevler başarıyla yüklendi:", tasks)
        return tasks
    except Exception as e:
        print(f"Görevler yüklenirken hata oluştu: {e}")
        return []

tasks = load_tasks()

@app.route('/')
def index():
    global current_task
    if current_task:
        # Eğer aktif bir görev varsa, o göreve yönlendir
        return redirect(url_for('task_page', task_id=current_task['id']))
    return render_template("index.html")

@app.route("/task/<task_id>")
def task_page(task_id):
    task = next((t for t in tasks if t["id"] == task_id), None)
    if task:
        return render_template("task.html", task=task)
    return "Görev bulunamadı", 404

@app.route("/get_current_task")
def get_current_task():
    global current_task
    return jsonify({"task": current_task})

@app.route("/reset_task")
def reset_task():
    global current_task
    current_task = None
    return redirect(url_for('index'))

def read_nfc():
    reader = SimpleMFRC522()
    global current_task
    
    print("NFC okuyucu başlatıldı ve hazır!")
    
    while True:
        try:
            print("Kart bekleniyor...")
            id, text = reader.read()  # Kartı oku
            print(f"Kart okundu! ID: {id}")
            
            # Kartın görevlerde olup olmadığını kontrol et
            task = next((t for t in tasks if str(t["nfc_uid"]) == str(id)), None)
            
            if task:
                print(f"Görev bulundu: {task['title']}")
                current_task = task
                last_task_queue.put(task)  # Kuyruğa görevi ekle
            else:
                print(f"Bu kart için ({id}) görev bulunamadı!")
                
            time.sleep(1)  # Kartın tekrar okunmasını önlemek için küçük bir bekleme
            
        except Exception as e:
            print(f"NFC okuma hatası: {e}")
            time.sleep(1)

def update_task_status():
    global current_task
    while True:
        try:
            # Kuyruktan yeni görev var mı kontrol et
            if not last_task_queue.empty():
                current_task = last_task_queue.get()
                print(f"Aktif görev güncellendi: {current_task['title']}")
        except Exception as e:
            print(f"Görev güncelleme hatası: {e}")
        time.sleep(0.1)

if __name__ == "__main__":
    try:
        # GPIO'yu temizle ve ayarla
        GPIO.cleanup()
        GPIO.setmode(GPIO.BOARD)
        
        # NFC okuma thread'ini başlat
        nfc_thread = threading.Thread(target=read_nfc, daemon=True)
        nfc_thread.start()
        print("NFC okuma thread'i başlatıldı")
        
        # Görev güncelleme thread'ini başlat
        update_thread = threading.Thread(target=update_task_status, daemon=True)
        update_thread.start()
        print("Görev güncelleme thread'i başlatıldı")
        
        # Flask uygulamasını başlat
        app.run(host="0.0.0.0", port=5000, debug=False)
        
    except Exception as e:
        print(f"Uygulama başlatılırken hata oluştu: {e}")
    finally:
        GPIO.cleanup()