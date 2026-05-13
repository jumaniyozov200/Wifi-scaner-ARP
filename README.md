# 🛡️ Professional ARP Spoofing va DNS Sniffer

Professional darajadagi Python va Scapy yordamida yasalgan ARP Spoofing va DNS Sniffing dasturi.

## 📋 Xulosa

Bu dastur tarmoqda Man-in-the-Middle (MITM) hujumi amalga oshirib, nishon qurilmaning barcha DNS so'rovlarini sniffer qiladi. Faqat ta'limiy va qonuniy penetration testing maqsadlarda ishlatilishi kerak.

### Asosiy Xususiyatlar

- 🔍 **Tarmoq Skanerlash** - ARP broadcast yordamida faol qurilmalarni topish
- 🎯 **Interaktiv Tanlash** - Foydalanuvchi nishoni va interfeysi tanlaydi
- 🌐 **ARP Spoofing** - Man-in-the-Middle (MITM) ochish
- 📡 **DNS Sniffing** - Nishon qurilmaning DNS so'rovlarini tutish
- 🔄 **ARP Restore** - To'xtatilganda asl holiga qaytarish
- 📊 **Statistika** - Hujumning natijalarini ko'rsatish
- 🇺🇿 **O'zbek Tili** - Barcha interfeys o'zbek tilida

## 🚀 Tez Ishga Tushirish

### O'rnatish

```bash
# Linux/macOS
sudo apt install python3-pip
pip install scapy

# Windows (Administrator PowerShell)
python -m pip install scapy
# Npcap'ni o'rnatish kerak: https://nmap.org/npcap/
```

### Ishga Tushirish

```bash
# Linux/macOS
sudo python3 arp_dns_sniffer.py

# Windows (Administrator PowerShell)
python arp_dns_sniffer.py
```

## 📖 Ishlatish Qo'llanmasi

### 1. Tarmoq Interfeysi Tanlash

```
📋 Mavjud interfeyslar:
  1. wlan0
  2. eth0
  3. docker0

🖱️  Raqamni tanlang (1-3): 1
```

### 2. Tarmoq Skanerlashi

Dastur avtomatik `192.168.1.0/24` tarmog'ini skanerlaydi va faol qurilmalarni ro'yxat qiladi:

```
✅ 192.168.1.50   | aa:bb:cc:dd:ee:01
✅ 192.168.1.75   | aa:bb:cc:dd:ee:02
✅ 192.168.1.99   | aa:bb:cc:dd:ee:03
```

### 3. Nishon Qurilmani Tanlash

Ro'yxatdan nishoni tanlang va gateway avtomatik topiladi.

### 4. Hujum Boshlanadi

ARP Spoofing va DNS Sniffing avtomatik boshlanadi. Nishon qurilmaning DNS so'rovlari real vaqtda chiqariladi:

```
🌐 [14:25:33] DNS so'rovi: google.com
🌐 [14:25:35] DNS so'rovi: youtube.com
🌐 [14:25:37] DNS so'rovi: facebook.com
```

### 5. Dasturni To'xtatish

**Ctrl+C** bosing. ARP jadvallar avtomatik qaytariladi va statistika chiqariladi:

```
📈 STATISTIKA
════════════════════════════════════════════
📤 Yuborilgan ARP paketlar: 324
📥 Sniffer qilingan DNS so'rovlar: 8
🌐 Har xil domenlar soni: 8
```

## 📚 Fayl Tuzilishi

```
arp-dns-sniffer/
├── arp_dns_sniffer.py       🛡️  Asosiy dastur
├── setup.py                  ⚙️  O'rnatish skripti
├── requirements.txt          📦 Kutubxonalar
├── DOKUMENTATSIYA.md         📖 Texnik dokumentatsiya
├── QUICKSTART.md             🚀 Tez ishga tushirish
└── README.md                 ℹ️  Bu fayl
```

## 🔧 Teknik Ma'lumotlar

### Qatlamlar (Layers)

| Qatlam | Nomi | Vazifasi |
|--------|------|----------|
| L2 | Ethernet | MAC manzillari (dst, src) |
| L3 | ARP/IP | IP va MAC moslashtirish |
| L4 | UDP | Port 53 (DNS) |
| L7 | DNS | Domain so'rovlari |

### Paket Tuzilishi

**ARP Spoofing Paket:**
```
Ether(dst=target_mac) / ARP(
    op="is-at",           # Reply
    pdst=target_ip,       # Nishon IP
    psrc=gateway_ip,      # Gateway IP (spoofed)
    hwsrc=our_mac,        # Bizning MAC
    hwdst=target_mac
)
```

**DNS Sniffing Filter:**
```
ip src {target_ip} and udp port 53
```

### MITM Jarayoni

```
Target ←→ Attacker ←→ Gateway
         (BIZLAR)
```

1. Nishon: Gateway → Attacker
2. Attacker: Gateway → Nishon
3. Barcha trafik attacker orqali o'tadi
4. Attacker DNS so'rovlarini sniffer qiladi

## ⚠️ Xavfsizlik Ogohlantirishi

### ✅ QONUNIY ISHLAT:

- ✓ O'zingizning test tarmoqida
- ✓ Ruxsatli penetration testing
- ✓ Cybersecurity o'rganish
- ✓ Tarmoq diagnostika

### ❌ ISHLATMASLIGI KERAK:

- ✗ Boshqa odamlarning qurilmalariga
- ✗ Malicious aktivlik
- ✗ Qonunsiz monitoringga
- ✗ Intellektual mulklarni o'g'irlanishiga

**BU DASTUR FAQAT EDUCATSIONAL VA QONUNIY MAQSADLARDA ISHLATILISHI KERAK.**

Noto'g'ri ishlat qilinsa, qonuniy javobgarlik to'lami kerak!

## 🔐 Muhim Xususiyatlar

1. **Scapy Verbose O'chgani** - `conf.verb = 0`
2. **MAC Manzili Aniqlanmasi** - `Ether(dst=target_mac)`
3. **Dublikat Filtri** - DNS cache yordamida
4. **ARP Restore** - 5 marta qayta jo'natish
5. **Signal Handler** - Ctrl+C to'xtatish

## 🛠️ Xatolar va Yechimlar

| Xato | Sababi | Yechim |
|------|--------|--------|
| PermissionError | Root yo'q | `sudo python3 ...` |
| ModuleNotFoundError | Scapy o'rnatilmagan | `pip install scapy` |
| No interface found | Interfeys noto'g'ri | `ifconfig` tekshiring |
| Gateway not found | Gateway offline | Ping qilib tekshiring |
| No packets | DNS so'rov yo'q | Browser ochib sahifa yuklang |

## 📊 Kutubxonalar

- **Scapy** - Packet manipulation
- **Python 3.7+** - Programming language
- **Threading** - Multi-threading uchun
- **Signal** - Graceful shutdown
- **Subprocess** - Interface detection

## 📝 Litsenziya

Bu loyiha educatsional maqsadlarda yaratilgan. Ishlatuvchi barcha javobgarlikni o'z zimmasiga oladi.

## 🤝 Hissa Qo'shish

Tuzatishlar, takliflar va yangi xususiyatlarni taklif qilishingiz mumkin.

## 📞 Qo'llab-Quvvatlash

Savollar bo'lsa:
1. DOKUMENTATSIYA.md'ni o'qing
2. QUICKSTART.md'dagi troubleshooting bo'limini ko'ring
3. Scapy dokumentatsiyasini tekshiring: https://scapy.readthedocs.io/

## 🎓 Keyingi Qadamlar

- CEH (Certified Ethical Hacker) sertifikati
- OSCP (Offensive Security) o'rganish
- Tarmoq xavfsizligi specialisti bo'lish
- Penetration testing muhassisi

## 📚 Tavsiya Etilgan Manbalar

- [Scapy Documentation](https://scapy.readthedocs.io/)
- [RFC 826 - ARP](https://tools.ietf.org/html/rfc826)
- [RFC 1035 - DNS](https://tools.ietf.org/html/rfc1035)
- [Wikipedia - MITM](https://en.wikipedia.org/wiki/Man-in-the-middle_attack)

---

**Yaratilgan:** 2024  
**Versiya:** 1.0  
**Maqsadi:** Cybersecurity ta'limi va tarmoq diagnostikasi  
**Til:** Python 3.7+  
**Litsenziya:** Educational Use Only

---

## 🎉 Tayyor!

Endi dasturni ishga tushirishingiz mumkin:

```bash
sudo python3 arp_dns_sniffer.py
```

**Omad tilaymiz! 🛡️**
