#!/bin/bash
# install.sh
# sudo chmod +x install.sh

echo "🎮 Hazine Avı Oyunu Kurulum Scripti"
echo "--------------------------------"

# Root kontrolü
if [ "$EUID" -ne 0 ]; then 
    echo "Bu script'i root olarak çalıştırmalısınız!"
    echo "Örnek: sudo ./install.sh"
    exit 1
fi

# Gerekli dizinlerin varlığını kontrol et
if [ ! -d "/home/pi/treasure-hunt" ]; then
    echo "Error: /home/pi/treasure-hunt dizini bulunamadı!"
    exit 1
fi

# Servis dosyasını kopyala
echo "Servis dosyası oluşturuluyor..."
cp treasure-hunt.service /etc/systemd/system/

# Yönetim script'ini kopyala
echo "Yönetim scripti kuruluyor..."
cp treasure-hunt /usr/local/bin/
chmod +x /usr/local/bin/treasure-hunt

# Servis'i etkinleştir
echo "Servis etkinleştiriliyor..."
systemctl enable treasure-hunt

# Log dizinini oluştur
mkdir -p /var/log/treasure-hunt
chown pi:pi /var/log/treasure-hunt

echo "Kurulum tamamlandı! ✓"
echo
echo "Kullanım:"
echo "  treasure-hunt start   : Servisi başlatır"
echo "  treasure-hunt stop    : Servisi durdurur"
echo "  treasure-hunt restart : Servisi yeniden başlatır"
echo "  treasure-hunt status  : Durumu gösterir"
echo "  treasure-hunt logs    : Logları gösterir"