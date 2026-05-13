# 🛡️ ARP Spoofing va DNS Sniffer - Texnik Dokumentatsiya

## 📋 Maqola Bo'yicha Xulosa

Bu loyiha **Python** va **Scapy** kutubxonasi yordamida professional darajadagi ARP Spoofing va DNS Sniffing dasturini amalga oshiradi.

---

## 🏗️ Arxitektura va Tuzilish

### 1. Asosiy Sinf: `ARPSpoofingDNSSniffer`

```python
class ARPSpoofingDNSSniffer:
    def __init__(self):
        self.target_ip = None          # Nishon IP manzili
        self.gateway_ip = None         # Gateway IP
        self.target_mac = None         # Nishon MAC manzili
        self.gateway_mac = None        # Gateway MAC
        self.interface = None          # Tarmoq interfeysi
        self.our_mac = None            # Bizning MAC manzili
        self.running = False           # Dastur holati
        self.packets_sent = 0          # Yuborilgan paketlar
        self.packets_sniffed = 0       # Sniffer qilingan paketlar
```

**Oxirgi o'zgaruvchilar:**
- `original_arp_table`: Asl ARP jadvallar (restore uchun)
- `dns_cache`: Sniffer qilingan domenlar (dublikat oldini olish)

---

## 🔧 Asosiy Funksiyalar

### 1️⃣ Tarmoq Skanerlash: `scan_network()`

**Vazifasi:** Mahalliy tarmoqdagi faol qurilmalarni aniqlash

```python
def scan_network(self):
    """
    ARP broadcast yordamida tarmoq skanerlash
    
    Qadamlar:
    1. Mahalliy IP manzilini olish
    2. CIDR notatsiyasi bilan tarmoq hisoblash (192.168.1.0/24)
    3. ARP broadcast yuborish (Ethernet broadcast)
    4. Javoblarni o'zbek tilida ko'rsatish
    
    Qaytarish: Qurilmalar ro'yxati (IP va MAC)
    """
```

**Misol:**
```
🔍 TARMOQ SKANERLASHI BOSHLANMOQDA
📡 Skanerlanyotgan tarmoq: 192.168.1.0/24
🔄 Skanerlash davom etmoqda...

✅ 192.168.1.50   | aa:bb:cc:dd:ee:01
✅ 192.168.1.75   | aa:bb:cc:dd:ee:02
```

---

### 2️⃣ ARP Spoofing: `spoof_arp()` va `spoof_process()`

**Vazifasi:** Man-in-the-Middle (MITM) ochish

```python
def spoof_arp(self, target_ip, spoof_ip):
    """
    ARP spoofing paketini yuborish
    
    Ether(dst=target_mac) / ARP(...) tuzilishi:
    ├─ Ether: Layer 2 (Data Link)
    │  └─ dst: Nishon MAC manzili (paketni to'g'ri joyga yo'naltirish)
    │
    └─ ARP: Address Resolution Protocol
       ├─ op="is-at": ARP reply (javob)
       ├─ pdst: Hamdaftarining IP (target_ip)
       ├─ psrc: Spoofed IP (gateway_ip)
       ├─ hwsrc: Bizning MAC (o'zgartirish)
       └─ hwdst: Nishon MAC
    """
```

**MITM Jarayoni:**
```
Nishon → 192.168.1.50
Gateway → 192.168.1.1

Paket almashinuvi:
┌─────────────────┐
│   Target (50)   │
└────────┬────────┘
         │ ARP: "192.168.1.1 is at MY_MAC"
         │ (Shuningdek gateway o'zi, lekin biz emas!)
         ↓
    ╔═════════════╗
    ║ BIZ (MITM)  ║  ← Barcha paketlar sizdан o'tadi
    ╚═════════════╝
         ↓
┌─────────────────┐
│ Gateway (1)     │
└─────────────────┘
```

**Har 1 soniyada 2 ta paket yuboriladi:**
1. Target'ga: "Gateway = Bizning MAC"
2. Gateway'ga: "Target = Bizning MAC"

---

### 3️⃣ DNS Sniffing: `packet_callback()` va `sniff_process()`

**Vazifasi:** DNS so'rovlarini tutish va aniqlashtirish

```python
def packet_callback(self, packet):
    """
    DNS paketini qayta ishlash
    
    Paket qatlamlar:
    IP
    ├─ src: Manba (faqat target_ip)
    └─ dst: Manzil
    
    UDP (Layer 4)
    ├─ sport: Manba port
    └─ dport: 53 (DNS)
    
    DNS
    ├─ qr: 0 = so'rov, 1 = javob
    └─ questions
        └─ qname: Domain nomi
    
    Misollar:
    - qr=0, qname='google.com' → "DNS so'rovi: google.com"
    - qr=1, qname='google.com' → Sniffer qilmamiz (javob)
    """
```

**Filtr:**
```python
sniff(
    filter=f"ip src {self.target_ip} and udp port 53",
    #        └─ Faqat nishon'dan
    #           └─ UDP 53-portida (DNS)
)
```

---

### 4️⃣ ARP Jadvallarini Restore: `restore_arp()`

**Vazifasi:** Hujumni to'xtatishda asl holiga qaytarish

```python
def restore_arp(self):
    """
    ARP qayta linglash (ARProtan asl qiymatlarni qaytarish)
    
    Asl holatga qaytish:
    ├─ Target: "192.168.1.1 is at Gateway_MAC" (real MAC)
    └─ Gateway: "192.168.1.50 is at Target_MAC" (real MAC)
    
    5 marta yuboriladi (ishonchlilik):
    └─ Graphy vaqt: ~0.5 soniya (jami 5 × 0.1s)
    """
```

**Asl holatga qaytganidan so'ng:**
- Nishon yana gateway'ga to'g'ri ulanadi
- Internet trafikni sizdān o'tish to'xtadi
- Foydalanuvchi kasal boladigan narsani sezmaydi

---

## 🔐 Xavfsizlik va Filtrlar

### 1. Verbose va Warning O'chiring
```python
conf.verb = 0  # Scapy ning barcha debug xabarlari o'chadi
```

### 2. O'zimizni Filtrlab Tashish
```python
if client_ip != local_ip:  # Scan natijalarda
    pass

if packet[IP].src == self.target_ip:  # DNS sniffingda
    pass
```

### 3. MAC Manzilini Aniq Ko'rsatish
```python
packet = Ether(dst=self.get_mac(target_ip)) / ARP(...)
         ^^^^^^
         Layer 2 (MAC) - kerak!
```

---

## 📊 Paket Tuzilishi Misollar

### ARP Request (Skanerlash)
```
┌─────────────────────────────────┐
│ Ethernet                        │
├─────────────────────────────────┤
│ dst: ff:ff:ff:ff:ff:ff (broadcast)
│ src: Bizning MAC
│ type: ARP (0x0806)
├─────────────────────────────────┤
│ ARP                             │
├─────────────────────────────────┤
│ op: 1 (request)
│ pdst: 192.168.1.50 (kiming MAC'i?)
└─────────────────────────────────┘
```

### ARP Reply (Spoofing)
```
┌─────────────────────────────────┐
│ Ethernet                        │
├─────────────────────────────────┤
│ dst: Target_MAC
│ src: Bizning MAC
│ type: ARP (0x0806)
├─────────────────────────────────┤
│ ARP                             │
├─────────────────────────────────┤
│ op: 2 (is-at/reply)
│ psrc: 192.168.1.1 (gateway)
│ hwsrc: Bizning MAC (SOXTA!)
│ pdst: 192.168.1.50 (target)
│ hwdst: Target_MAC
└─────────────────────────────────┘

🎯 Natijai: Target ARP jadvali:
   192.168.1.1 → Bizning MAC (XATO!)
   (To'g'ri javob: Gateway MAC)
```

### DNS Query Paket
```
┌─────────────────────────────────┐
│ Ethernet                        │
├─────────────────────────────────┤
│ dst: Gateway_MAC
│ src: Target_MAC
├─────────────────────────────────┤
│ IP                              │
├─────────────────────────────────┤
│ src: 192.168.1.50 (target)
│ dst: 192.168.1.1 (gateway/DNS)
├─────────────────────────────────┤
│ UDP                             │
├─────────────────────────────────┤
│ sport: 54321
│ dport: 53 (DNS)
├─────────────────────────────────┤
│ DNS                             │
├─────────────────────────────────┤
│ qr: 0 (query)
│ qname: google.com
└─────────────────────────────────┘

📊 Sniffer natijasi:
   "DNS so'rovi: google.com"
```

---

## ⚙️ Qatlamlar va Protokollar

| Qatlam | Nomi | Funktsiya |
|--------|------|-----------|
| L1 | Physical | Kabel, o'tkir |
| **L2** | **Ethernet/MAC** | **Ether(dst=MAC)** |
| **L3** | **IP** | **IP(src, dst)** |
| **L4** | **UDP** | **UDP(sport, dport)** |
| **L7** | **DNS** | **DNSQR(qname)** |

**Scapy'da Stack:**
```python
packet = Ether() / ARP()           # L2 + L3.5
packet = Ether() / IP() / UDP()    # L2 + L3 + L4
packet = Ether() / IP() / UDP() / DNS()  # L2 + L3 + L4 + L7
```

---

## 🔄 Jarayoni Tashkil Etish

```
MAIN (Asosiy thread)
├─ select_interface()     ← Interfeys tanlash
├─ scan_network()         ← Tarmoq skanerlash
├─ select_target()        ← Nishon tanlash
│
└─ THREAD 1: spoof_process()   (daemon=True)
│  ├─ Har 1 soniyada spoof_arp() chaqirish
│  ├─ Target → Gateway
│  ├─ Gateway → Target
│  └─ self.running = True qo'lingan bo'lguncha
│
└─ THREAD 2: sniff_process()   (daemon=True)
   └─ Paketlarni tutish (filter yordamida)
      ├─ IP src == target_ip
      ├─ UDP dport == 53 (DNS)
      ├─ DNS qr == 0 (so'rov)
      └─ packet_callback() chaqirish

Signal: Ctrl+C
   ↓
signal_handler()
   ├─ self.running = False (threadlari to'xtatish)
   ├─ restore_arp() (5 marta yuborish)
   ├─ print_statistics() (natijalar)
   └─ sys.exit(0)
```

---

## 💾 Holatlar (States)

```
START
  ├─ Interface selection → INTERFACE_SELECTED
  ├─ Scan network → DEVICES_FOUND
  ├─ Select target → TARGET_SELECTED
  │
  ├─ Spawn threads
  └─ Set self.running = True
       │
       ├─ SPOOFING_ACTIVE
       │  └─ ARP paketlari yuborilmoqda
       │
       ├─ SNIFFING_ACTIVE
       │  └─ DNS paketlari sniffer qilinmoqda
       │
       ├─ Ctrl+C pressed
       └─ CLEANUP
           ├─ Set self.running = False
           ├─ restore_arp() (5 ta paket)
           └─ EXIT
```

---

## 📈 Statistika va Monitoring

```python
self.packets_sent          # ARP spoofing paketlari soni
self.packets_sniffed       # DNS so'rovlari soni
self.dns_cache             # {domain: True, ...}

print_statistics():
   ├─ 📤 Yuborilgan ARP paketlar: 324
   ├─ 📥 Sniffer qilingan DNS so'rovlar: 12
   ├─ 🌐 Har xil domenlar soni: 8
   └─ 🌐 Ziyarat qilingan domenlar:
        1. google.com
        2. youtube.com
        3. facebook.com
        4. instagram.com
        5. twitter.com
        6. github.com
        7. stackoverflow.com
        8. linkedin.com
```

---

## 🛠️ Tuzatish va Optimization

### Masalalar va Yechimlar

| Muammo | Sabab | Yechim |
|--------|-------|--------|
| "PermissionError" | Root huquqi yo'q | `sudo python3 ...` |
| "No packets" | Interface noto'g'ri | `ifconfig` bilan tekshirish |
| "Gateway not found" | Gateway offline | Gateway faolligini tekshirish |
| "Low packet rate" | Juda ko'p ARP | Intervalni orttirib ko'ring |
| "Errors in output" | Scapy verbose | `conf.verb = 0` (bajarilgan) |

### Performance Optimization

```python
# 1. Paket jo'natish tezligi
threading.Event().wait(1)  # Har 1 soniyada (o'zgartirilishi mumkin)

# 2. DNS cache
self.dns_cache = {}  # Dublikat so'rovlarni to'xtata oladi

# 3. Sniff filter
filter="ip src {target_ip} and udp port 53"
# Butun paketlarni tekshirish o'rniga
# Faqat mos paketlarni tutadi

# 4. Thread daemon
thread = threading.Thread(..., daemon=True)
# Main thread to'xtasa, uzoq threadlar ham to'xtadi
```

---

## 📚 Scapy Kutubxonasi O'ziga Xos Kodlari

```python
# Paket yuborish (Layer 2 - MAC)
from scapy.all import sendp
sendp(packet, iface="wlan0")

# ARP broadcast
Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst="192.168.1.0/24")

# Paketlarni tutish
sniff(iface="wlan0", prn=callback, filter="udp port 53")

# MAC manzili topish
srp(ARP_packet, iface="wlan0", timeout=2)  # Send and receive

# Interfeys MAC'i
get_if_hwaddr("wlan0")

# Interfeys IP'i
get_if_addr("wlan0")
```

---

## ✅ Barcha Talablarning Bajarilishi

| # | Talaba | Holati | Tushuntirish |
|---|--------|--------|--------------|
| 1 | Tarmoq skanerlash | ✅ Bajarildi | `scan_network()` - ARP broadcast |
| 2 | Interfeyni sozlash | ✅ Bajarildi | `select_interface()` - interaktiv |
| 3 | ARP Spoofing (L2) | ✅ Bajarildi | `Ether(dst=MAC)` aniq ko'rsatilgan |
| 4 | DNS Sniffing | ✅ Bajarildi | `packet_callback()` - UDP 53 |
| 5 | Xatolik boshqarish | ✅ Bajarildi | `conf.verb=0`, try-except |
| 6 | ARP Restore | ✅ Bajarildi | `restore_arp()` - 5 marta yuborish |
| 7 | O'zbek tili | ✅ Bajarildi | Barcha print xabarlari |

---

## 🎓 Qo'shimcha Bilim

### ARP Spoofing Muxlisi

ARP (Address Resolution Protocol) IP manzilini MAC manzilga o'tkazadi:
```
"192.168.1.1 kimning MAC'iga?"
→ "00:11:22:33:44:55"

Spoofing:
"192.168.1.1 MENNING MAC'iga!" (shuningdek emas)
→ "AA:BB:CC:DD:EE:FF" (bizning MAC)

Natijai: Target bizni gateway deb hisoblaydi
```

### DNS Sniffing Usuli

DNS so'rovlar Plaintext (shifrlash yo'q):
```
Attacker → Target'ni MITM qilish
         → Barcha paketlari ko'rish
         → DNS so'rovlarni yozib olish
         → Ularni tahlil qilish
```

### MITM Jarayoni

```
┌────────┐   ┌────────┐   ┌────────┐
│ Target │ ↔ │ Attacker│ ↔ │Gateway │
└────────┘   │(BIZLAR)│   └────────┘
             └────────┘

1. Target: Gateway'dan gapiradi → Attacker
2. Attacker: Gateway'ga yubor → Gateway
3. Gateway: Target'dan javob → Attacker
4. Attacker: Target'ga yubor → Target
```

---

## 📝 Litsenziya va Etika

⚠️ **BU DASTUR FAQAT:**
- O'zingizning tarmoqida
- Qonuniy maqsadlarda
- Testlash va o'rganish uchun

**ISHLATMASLIGI KERAK:**
- Boshqalarning qurilmalariga
- Malicious aktivlik uchun
- Qonunsiz monitoringga

---

## 🔗 Foydali Manbalar

- [Scapy Documentation](https://scapy.readthedocs.io/)
- [ARP Protocol RFC 826](https://tools.ietf.org/html/rfc826)
- [DNS Protocol RFC 1035](https://tools.ietf.org/html/rfc1035)
- [Man-in-the-Middle Attacks](https://en.wikipedia.org/wiki/Man-in-the-middle_attack)

---

**Yaratilgan sana:** 2024
**Versiya:** 1.0
**Maqsadi:** Cybersecurity ta'limi va tarmoq diagnostikasi
