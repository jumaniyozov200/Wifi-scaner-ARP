#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🛡️ ARP SPOOFING VA DNS SNIFFER - TEZ ISHGA TUSHIRISH QOLLANMASI
═══════════════════════════════════════════════════════════════════════════════
"""

# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║ 1. O'RNATISH (INSTALLATION)                                               ║
# ╚═══════════════════════════════════════════════════════════════════════════╝

print("""
┌───────────────────────────────────────────────────────────────────────────┐
│                          ⬇️  O'RNATISH QADAMLARI                           │
└───────────────────────────────────────────────────────────────────────────┘

1️⃣  KALI LINUX / UBUNTU / DEBIAN:
    ─────────────────────────────────

    $ sudo apt update
    $ sudo apt install python3 python3-pip
    $ pip install scapy
    
    Masalan:
    $ pip install --upgrade scapy

2️⃣  CENTOS / FEDORA / RHEL:
    ────────────────────────

    $ sudo dnf install python3 python3-pip
    $ pip install scapy

3️⃣  macOS:
    ────────

    $ brew install python3
    $ pip3 install scapy

4️⃣  WINDOWS (Administrator PowerShell):
    ────────────────────────────────────

    > python -m pip install --upgrade pip
    > pip install scapy
    
    ⚠️  Npcap driver o'rnatish kerak:
    https://nmap.org/npcap/

═════════════════════════════════════════════════════════════════════════════
""")


# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║ 2. BAJARILISHI (EXECUTION)                                                ║
# ╚═══════════════════════════════════════════════════════════════════════════╝

print("""
┌───────────────────────────────────────────────────────────────────────────┐
│                        🚀 DASTURNI ISHGA TUSHIRISH                        │
└───────────────────────────────────────────────────────────────────────────┘

LINUX / macOS:
──────────────

    $ sudo python3 arp_dns_sniffer.py

    YOKI (Agar scapy o'rnatilmagan bo'lsa):
    
    $ sudo python3 setup.py


WINDOWS (Administrator PowerShell):
────────────────────────────────

    > python arp_dns_sniffer.py


DOCKER (Opsional):
──────────────────

    $ docker run -it --rm \\
        --privileged \\
        -v $(pwd):/app \\
        -w /app \\
        python:3.11 \\
        bash -c "pip install scapy && python3 arp_dns_sniffer.py"

═════════════════════════════════════════════════════════════════════════════
""")


# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║ 3. ISHNING KETISHI (WORKFLOW)                                             ║
# ╚═══════════════════════════════════════════════════════════════════════════╝

print("""
┌───────────────────────────────────────────────────────────────────────────┐
│                         📊 DASTUR ISHINING KETISHI                        │
└───────────────────────────────────────────────────────────────────────────┘

QADAMI 1: INTERFEYS TANLASH
───────────────────────────

    Siz ko'rasiz:
    ┌─────────────────────────────────────────┐
    │ 📋 Mavjud interfeyslar:                 │
    │   1. wlan0                              │
    │   2. eth0                               │
    │   3. docker0                            │
    │                                         │
    │ 🖱️  Raqamni tanlang (1-3): █            │
    └─────────────────────────────────────────┘
    
    Siz kiritasiz:
    >>> 1
    
    Natija:
    ✅ Tanlangan interfeys: wlan0
       MAC manzili: aa:bb:cc:dd:ee:ff


QADAMI 2: TARMOQ SKANERLASHI
────────────────────────────

    Dastur avtomatik skanerlaydi:
    
    🔍 TARMOQ SKANERLASHI BOSHLANMOQDA
    📡 Skanerlanyotgan tarmoq: 192.168.1.0/24
    📍 Mahalliy IP: 192.168.1.100
    🔄 Skanerlash davom etmoqda...
    
    ✅ 192.168.1.1    | 00:11:22:33:44:55  (Gateway)
    ✅ 192.168.1.50   | aa:bb:cc:dd:ee:01  (Telefon)
    ✅ 192.168.1.75   | aa:bb:cc:dd:ee:02  (Kompyuter)
    ✅ 192.168.1.99   | aa:bb:cc:dd:ee:03  (Printer)
    
    📊 Jami qurilmalar: 4


QADAMI 3: NISHON QURILMANI TANLASH
──────────────────────────────────

    🎯 NISHON QURILMANI TANLANG
    📍 Gateway IP: 192.168.1.1
    
    📋 Mavjud qurilmalar:
      1. 192.168.1.50   | aa:bb:cc:dd:ee:01
      2. 192.168.1.75   | aa:bb:cc:dd:ee:02
      3. 192.168.1.99   | aa:bb:cc:dd:ee:03
    
    🖱️  Raqamni tanlang (1-3): █
    
    Siz kiritasiz:
    >>> 1
    
    Natija:
    ✅ Nishon tanlandi:
       IP: 192.168.1.50
       MAC: aa:bb:cc:dd:ee:01


QADAMI 4: ARP SPOOFING VA DNS SNIFFING
─────────────────────────────────────

    Dastur avtomatik hujum boshlamadi:
    
    🚀 ARP SPOOFING JARAYONI BOSHLANMOQDA
    ════════════════════════════════════════════
    
    📊 DNS SNIFFING BOSHLANMOQDA
    ════════════════════════════════════════════
    
    🌐 Nishon qurilmadan keladigan DNS so'rovlari:
    
    🌐 [14:25:33] DNS so'rovi: google.com
    🌐 [14:25:35] DNS so'rovi: youtube.com
    🌐 [14:25:37] DNS so'rovi: facebook.com
    🌐 [14:25:40] DNS so'rovi: instagram.com
    🌐 [14:25:42] DNS so'rovi: twitter.com
    🌐 [14:25:45] DNS so'rovi: github.com
    🌐 [14:25:48] DNS so'rovi: stackoverflow.com
    
    (Nishon qurilma Internetga kirayotgan o'zgarishlar)
    
    ⏰ HUJUM KETMOQDA...
    
    Dastur Ctrl+C ni kutmoqda


QADAMI 5: TO'XTATISH VA RESTORE
───────────────────────────────

    Keyboard'dan Ctrl+C bosing:
    
    >>> Ctrl+C
    
    ⏹️  DASTUR TO'XTATILMOQDA...
    🔄 ARP JADVALLARINI QAYTARILMOQDA...
    ✅ ARP jadvallar qaytarildi!
    
    ════════════════════════════════════════════
    📈 STATISTIKA
    ════════════════════════════════════════════
    📤 Yuborilgan ARP paketlar: 324
    📥 Sniffer qilingan DNS so'rovlar: 8
    🌐 Har xil domenlar soni: 8
    
    🌐 Ziyarat qilingan domenlar:
       1. google.com
       2. youtube.com
       3. facebook.com
       4. instagram.com
       5. twitter.com
       6. github.com
       7. stackoverflow.com
       8. linkedin.com

═════════════════════════════════════════════════════════════════════════════
""")


# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║ 4. MUHIM BILGILER (IMPORTANT INFO)                                        ║
# ╚═══════════════════════════════════════════════════════════════════════════╝

print("""
┌───────────────────────────────────────────────────────────────────────────┐
│                          ⚠️  MUHIM OGOHLANTIRISH                          │
└───────────────────────────────────────────────────────────────────────────┘

1. ROOT/ADMINISTRATOR HUQUQI KERAK
   ────────────────────────────────
   
   ❌ Xato:        python3 arp_dns_sniffer.py
   ✅ To'g'ri:      sudo python3 arp_dns_sniffer.py
                   (Linux/macOS uchun)

2. NISHON VA GATEWAY BIR TARMOQDA BO'LISHI KERAK
   ───────────────────────────────────────────────
   
   Masalan:
   ✅ Siz: 192.168.1.100
   ✅ Nishon: 192.168.1.50
   ✅ Gateway: 192.168.1.1
   
   ❌ Siz: 10.0.0.100
   ❌ Nishon: 192.168.1.50  ← BOSHQA TARMOQ!

3. FIREWALL/ANTIVIRUS MUAMMOSI
   ──────────────────────────────
   
   Agar paketlar o'tmasalar:
   - Firewall ni o'chib ko'ring
   - Antivirus'ni o'chib ko'ring
   - Sudo bilan ishga tushiring

4. SCAPY KUTUBXONASI KERAK
   ────────────────────────
   
   $ pip install scapy
   
   Agar "ModuleNotFoundError: No module named 'scapy'" chiqsa

5. QANUNIY ISHLAT FAQAT
   ─────────────────────
   
   ✅ O'zingizning test tarmoqida
   ✅ Ruxsatli penetration testing
   ✅ Educatsional maqsadlarda
   
   ❌ Boshqalarning qurilmalariga
   ❌ Malicious aktivlik uchun
   ❌ Qonunsiz monitoring

═════════════════════════════════════════════════════════════════════════════
""")


# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║ 5. XATOLAR VA YECHIMLAR (TROUBLESHOOTING)                                 ║
# ╚═══════════════════════════════════════════════════════════════════════════╝

print("""
┌───────────────────────────────────────────────────────────────────────────┐
│                        🔧 XATOLAR VA YECHIMLAR                            │
└───────────────────────────────────────────────────────────────────────────┘

❌ XATO #1: "PermissionError: Operation not permitted"
─────────────────────────────────────────────────────

Sababi:  Root huquqi yo'q

Yechim:  sudo bilan ishga tushiring
         $ sudo python3 arp_dns_sniffer.py


❌ XATO #2: "ModuleNotFoundError: No module named 'scapy'"
──────────────────────────────────────────────────────

Sababi:  Scapy o'rnatilmagan

Yechim:  $ pip install scapy
         YOKI
         $ pip install --upgrade scapy


❌ XATO #3: "No interface found"
────────────────────────────────

Sababi:  Interfeys mavjud emas

Yechim:  Interfeysingizni tekshiring:
         $ ifconfig (Linux/macOS)
         > ipconfig (Windows)
         
         Raqamni to'g'ri kiritganligini tekshiring


❌ XATO #4: "Gateway MAC not found"
───────────────────────────────────

Sababi:  Gateway offline yoki ARP'ga javob bermayapti

Yechim:  Gateway'ning IP'ini tekshiring
         Gateway'ni ping qilib ko'ring:
         $ ping 192.168.1.1
         
         Agar javob bo'lmasa, gateway offline


❌ XATO #5: "No packets captured"
─────────────────────────────────

Sababi:  Nishon qurilma DNS so'rovlari yo'lmadi

Yechim:  Nishon qurilmada browser ochib, sahifa yuklang
         Masalan: nishon telefonda YouTube yuklash
         
         Agar hali ham paket yo'lmasa:
         - Firewall'ni tekshiring
         - VPN yoki proxy bilan ulanishi tekshiring
         - Ish rejimini sinab ko'ring


❌ XATO #6: "WARNING: bad reception, many duplicate packets received"
───────────────────────────────────────────────────────────────────

Sababi:  Juda ko'p paketlar yuborilmoqda

Yechim:  spoof_process() dagi wait vaqtini orttirib ko'ring:
         
         threading.Event().wait(2)  # 1 o'rniga 2 soniya


❌ XATO #7: "Cannot find device for 192.168.1.50"
─────────────────────────────────────────────────

Sababi:  Nishon qurilma tarmog'da yo'q yoki offline

Yechim:  Qurilmani taqqoslang va qayta tanlang
         Nishon qurilmani ping qilib ko'ring


❌ XATO #8: WINDOWS DA HUJUM ISHLAMADI
──────────────────────────────────────

Sababi:  Raw socket yoki Npcap driver yo'q

Yechim:  1. Npcap'ni o'rnatish (Administrator):
            https://nmap.org/npcap/
         
         2. Administrator PowerShell bilan ishga tushirish
         
         3. Scapyni qayta o'rnatish:
            > pip install --force-reinstall scapy

═════════════════════════════════════════════════════════════════════════════
""")


# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║ 6. ADVANCED FOYDALANISH (ADVANCED USAGE)                                  ║
# ╚═══════════════════════════════════════════════════════════════════════════╝

print("""
┌───────────────────────────────────────────────────────────────────────────┐
│                        🚀 ADVANCED FOYDALANISH                            │
└───────────────────────────────────────────────────────────────────────────┘

1. MULTIPLE TARGETS (Bir vaqtada ko'p nishon)
───────────────────────────────────────────

   # Kod o'zgartirib:
   targets = ["192.168.1.50", "192.168.1.75", "192.168.1.99"]
   
   for target in targets:
       sniffer = ARPSpoofingDNSSniffer()
       sniffer.target_ip = target
       # Spoofing va sniffing...


2. PORT BASED FILTERING (Boshqa portlarni sniffing)
───────────────────────────────────────────────────

   filter="ip src {target_ip} and udp"
   # Barcha UDP portlarni
   
   filter="ip src {target_ip} and tcp port 80"
   # Faqat HTTP (port 80)


3. OUTPUT TO FILE (Natijalarni fayl'ga saqlash)
───────────────────────────────────────────────

   with open("sniffer_results.txt", "a") as f:
       f.write(f"[{timestamp}] {domain}\n")


4. JSON FORMAT OUTPUT
──────────────────────

   import json
   
   results = {
       "timestamp": datetime.now().isoformat(),
       "target_ip": self.target_ip,
       "packets_sent": self.packets_sent,
       "domains": list(self.dns_cache.keys())
   }
   
   with open("results.json", "w") as f:
       json.dump(results, f, indent=2)


5. SCAPY FILTER QOIDALARI
─────────────────────────

   # IP filteri
   filter="ip src 192.168.1.50"
   
   # UDP filteri
   filter="udp"
   
   # Port filteri
   filter="tcp port 80"
   filter="udp port 53"
   
   # Murakkab filterlar
   filter="ip src 192.168.1.0/24 and udp port 53"
   filter="(tcp port 80 or tcp port 443) and dst 192.168.1.1"

═════════════════════════════════════════════════════════════════════════════
""")


# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║ 7. FAYL TUZILISHI (FILE STRUCTURE)                                        ║
# ╚═══════════════════════════════════════════════════════════════════════════╝

print("""
┌───────────────────────────────────────────────────────────────────────────┐
│                         📁 FAYL TUZILISHI                                 │
└───────────────────────────────────────────────────────────────────────────┘

Proyekt papkasi:
─────────────────

arp-dns-sniffer/
├── arp_dns_sniffer.py          🛡️  Asosiy dastur
├── setup.py                     ⚙️  O'rnatish skripti
├── DOKUMENTATSIYA.md            📚 Detal teknik dokumentatsiya
├── QUICKSTART.md                📖 Bu fayl
├── README.md                    ℹ️  Umumiy ma'lumot
└── requirements.txt             📦 Kutubxonalar ro'yxati
    scapy>=2.4.5
    (Mahalliy o'rnatish uchun: pip install -r requirements.txt)


Fayl o'lchamlari:
────────────────

arp_dns_sniffer.py              ~15 KB
setup.py                         ~8 KB
DOKUMENTATSIYA.md                ~25 KB
QUICKSTART.md                    ~20 KB


Python versiyasi:
─────────────────

Python 3.7+  ← Talab
Python 3.8   ← Tavsiya etiladi
Python 3.9   ← Eng yaxshi
Python 3.10+ ← Yangi versiyalar

═════════════════════════════════════════════════════════════════════════════
""")


# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║ 8. XULOSA VA KEYINGI QADAMLAR (SUMMARY & NEXT STEPS)                      ║
# ╚═══════════════════════════════════════════════════════════════════════════╝

print("""
┌───────────────────────────────────────────────────────────────────────────┐
│                         ✅ XULOSA VA KEYINGI QADAMLAR                     │
└───────────────────────────────────────────────────────────────────────────┘

🎯 BAJARILGAN NARSALAR:
──────────────────────

✅ Tarmoq skanerlash (ARP broadcast)
✅ Faol qurilmalarni aniqlash
✅ Interaktiv nishon tanlash
✅ ARP Spoofing (MITM ochish)
✅ DNS Sniffing (so'rovlarni tutish)
✅ ARP Restore (hujumni asl holiga qaytarish)
✅ Statistika va monitoring
✅ O'zbek til interface
✅ Barcha xatolarni boshqarish
✅ Ctrl+C yordamida to'xtatish


📚 KEYINGI O'RGANILADIGAN NARSALAR:
───────────────────────────────────

1. TRAFFIC ANALYSIS (Tarmoq tahlili)
   - Tcpdump / Wireshark bilan paketlarni tahlil qilish
   - Trafik grafiklari
   - Paket dekodlash

2. ADVANCED MITM
   - SSL stripping
   - DNS hijacking
   - Cookie stealing

3. PACKET INJECTION
   - Paketlarni o'zgartirish
   - Shaxsiy paketlar yuborish
   - Protocol fuzzing

4. NETWORK SECURITY
   - Firewall qoidalari
   - IDS/IPS (Intrusion Detection)
   - Encryption va TLS

5. PYTHON OPTIMIZATION
   - Async paketlar
   - Multi-processing
   - Real-time visualization


📖 TAVSIYA ETILGAN MATERIALLAR:
──────────────────────────────

1. Scapy Official Docs
   https://scapy.readthedocs.io/

2. Ethical Hacking & Penetration Testing
   https://www.elearnsecurity.com/

3. Network Protocols
   - RFC 826 (ARP)
   - RFC 1035 (DNS)
   - RFC 791 (IPv4)

4. YouTube Kanallar
   - NetworkChuck
   - John Hammond
   - Liveoverflow


🚀 LOYIHANI KENGAYTIRISH:
────────────────────────

1. GUI Interface (PyQt/Tkinter)
2. Database saqlash (SQLite)
3. Export (CSV, JSON, XML)
4. Web Dashboard
5. Mobile Application
6. Cloud Integration


💡 OPTIMIZATSIYA VARIANTLARI:
──────────────────────────────

Vaqt qisqartirish:
  - Threading optimallashtirish
  - Async paketlar
  - C extension (Cython)

Xotira kamaytirib:
  - Generator functions
  - Streaming processing
  - Data compression

Tezlik oshirib:
  - PyPy interpreter
  - C/C++ bindings
  - FPGA acceleration


═════════════════════════════════════════════════════════════════════════════

🎓 SERTIFIKATLASH VA KASBIY RIVOJLANISH:
──────────────────────────────────────────

Ushbu loyihani yakunlagandan so'ng:
  ✓ CEH (Certified Ethical Hacker)
  ✓ OSCP (Offensive Security Certified Professional)
  ✓ CompTIA Security+
  ✓ Network+ 
  Sertifikatlari uchun tayyorlashtira olasiz.


═════════════════════════════════════════════════════════════════════════════
                              🎉 TAYYOR!

             Endi dasturni ishga tushirishingiz va o'rganishingiz mumkin!

                    $ sudo python3 arp_dns_sniffer.py

═════════════════════════════════════════════════════════════════════════════
""")

if __name__ == "__main__":
    print("\n✅ TEZ ISHGA TUSHIRISH QOLLANMASI TUGATILDI\n")
    print("📁 Boshqa fayllarni ko'ring:")
    print("   • arp_dns_sniffer.py - Asosiy dastur")
    print("   • setup.py - O'rnatish va kutubxonalar")
    print("   • DOKUMENTATSIYA.md - Detal teknik ma'lumot")
    print("   • README.md - Umumiy ma'lumot\n")
