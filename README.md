# treasure-hunt

# Hazine Avı NFC Kart Oyunu

Bu proje, bir Raspberry Pi ve NFC okuyucu kullanarak, çocuklar için interaktif bir hazine avı oyunu oluşturur. Kart okutulduğunda, çocuğu yönlendiren ve eğlendiren görev sayfalarına otomatik olarak yönlendirilir.

## Özellikler

- **NFC Kart Okuma**: NFC kart okutulduğunda, kartın ID'sine göre belirlenmiş görev sayfasına yönlendirme yapılır.
- **Otomatik Yönlendirme**: Kart okutulduktan sonra görev sayfasına otomatik yönlendirme yapılır.
- **Görev Yönetimi**: Görevler bir JSON dosyasında saklanır ve kolayca güncellenebilir.
- **Dosya Tabanlı ID Depolama**: Son okutulan `task_id`, bir dosyada saklanır ve Flask tarafından kontrol edilerek yönlendirme sağlanır.

## Gereksinimler

- Raspberry Pi cihazı
- MFRC522 NFC Kart Okuyucu
- Python 3.x
- Gerekli Python kütüphaneleri:
  - Flask
  - RPi.GPIO
  - mfrc522

## Kurulum

1. **Gerekli kütüphaneleri yükleyin**:

    ```bash
    pip install flask RPi.GPIO mfrc522
    ```
    or 
    ```bash
    pip install -r requirements.txt
    ```

2. **Proje dosyalarını indirin veya klonlayın**:

    ```bash
    git clone https://github.com/eakayoglu/treasure-hunt.git
    cd treasure-hunt
    ```

3. **Görevleri tanımlayın**: 

    - Kart ID leri bilinmiyorsa, `read_nfc/id_reader.py`kullanılarak kart ID leri `card_ids.txt` dosyasına kaydedilir.
    - `static/videos/` klasörü altına videoları ekleyin
    - `static/tasks.json` dosyasını düzenleyerek alınan kart ID leri ve yüklenen video URL lerini güncelleyin.
    - `static/tasks.json` dosyasının içeriğini istediğiniz şekilde güncelleyebilir ya da yeni kayıtlar ekleyerek uygulamayı genişletebilirsiniz!


4. **Flask Sunucusunu Başlatın**:

    ```bash
    flask run --host=0.0.0.0
    ```
    or 
    ```bash
    python app.py
    ```

## Dosya Yapısı

- `app.py`: Flask sunucusunu ve NFC kart okuma işlevini içerir.
- `static/tasks.json`: Her NFC kart ID'sine karşılık gelen görevleri içeren JSON dosyası.
- `templates/index.html`: Ana sayfa, NFC kart okutulduktan sonra otomatik olarak görev sayfasına yönlendirme yapılmasını sağlar.
- `templates/task.html`: Her görevin görüntülendiği sayfa şablonu.
- `last_task_id.txt`: Son okutulan kartın görev ID'sini depolar.

## Kullanım

1. **Kart Okutma**: Raspberry Pi'ye bağlı NFC okuyucuya bir kart okutun.
2. **Göreve Yönlendirme**: Kart okutulduğunda, ilgili göreve otomatik olarak yönlendirilirsiniz.

## Notlar

- Bu proje bir eğitim/eğlence projesidir ve gelişmiş güvenlik veya optimizasyonlar içermemektedir.
- NFC kart ID’leri her okutulduğunda, `last_task_id.txt` dosyasına yazılır ve Flask uygulaması bu dosyayı kontrol ederek yönlendirme sağlar.
- Bu proje Raspberry Pi üzerinde çalışmak üzere tasarlanmıştır.

## Katkıda Bulunma

Katkıda bulunmak isterseniz lütfen bir **Pull Request** gönderin veya bir **Issue** açın.

## Lisans

Bu proje MIT Lisansı ile lisanslanmıştır.

Bu README.md dosyası, proje hakkında bilgi verir, kurulum ve kullanım talimatlarını içerir. Projenizi GitHub’da yayımlarken ekleyebilirsiniz.