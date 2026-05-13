#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARP Spoofing va DNS Sniffer Dasturi - O'rnatish Skripti
"""

import subprocess
import sys
import platform

def install_dependencies():
    """Kerakli kutubxonalarni o'rnatish"""
    
    print("\n" + "="*70)
    print("📦 KERAKLI KUTUBXONALARNI O'RNATISH")
    print("="*70)
    
    packages = [
        "scapy>=2.4.5"
    ]
    
    print("\n🔧 Scapy kutubxonasini o'rnatishga harakat qilinyapti...")
    
    try:
        for package in packages:
            print(f"\n⬇️  {package} o'rnatilmoqda...")
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", 
                "--upgrade", package
            ])
            print(f"✅ {package} o'rnatildi!")
        
        print("\n" + "="*70)
        print("✅ BARCHA KUTUBXONALAR O'RNATILDI!")
        print("="*70)
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ O'rnatish xatosi: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Xato: {e}")
        sys.exit(1)


def print_instructions():
    """Ishlatish ko'rsatmalari"""
    
    instructions = """
╔═══════════════════════════════════════════════════════════════════════════╗
║           🛡️  ARP SPOOFING VA DNS SNIFFER - ISHLATISH KO'RSATMALARI       ║
╚═══════════════════════════════════════════════════════════════════════════╝

📋 TALABLAR:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  • Linux yoki macOS tizimni (Kali Linux tavsiya etiladi)
  • Administrator/Root huquqi
  • Python 3.7+
  • Scapy kutubxonasi
  • Nishon qurilma bir xil tarmoqda bo'lishi kerak

🚀 ISHGA TUSHIRISH:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1️⃣  LINUX/macOS DA:
   
   $ sudo python3 arp_dns_sniffer.py
   
   yoki
   
   $ sudo python3 -m pip install scapy
   $ sudo python3 arp_dns_sniffer.py

2️⃣  WINDOWS DA (Administrator bilan PowerShell):
   
   > python arp_dns_sniffer.py

📊 DASTUR QANDAY ISHLAYDI:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  1. Tarmoq Interfeysini Tanlash
     └─ Mavjud interfeyslar ko'rsatiladi (wlan0, eth0, va h.k.)
     └─ Raqamni kiritib, interfeysni tanlaysiz

  2. Tarmoq Skanerlashi
     └─ 192.168.1.0/24 tarmog'iga ARP broadcast yuboriladi
     └─ Faol qurilmalar va ularning MAC manzillari chiqariladi

  3. Nishon Qurilmani Tanlash
     └─ Skanerlangan qurilmalar ro'yxatidan nishoni tanlaysiz
     └─ Avtomatik Gateway IP topiladi

  4. ARP Spoofing Boshlanadi
     └─ Nishon va Gateway o'rtasida Man-in-the-Middle (MITM) ochiladi
     └─ Barcha internet trafiksi sizdан o'tadi

  5. DNS Sniffing Boshlanadi
     └─ Nishon qurilmaning barcha DNS so'rovlari sniffer qilinadi
     └─ Qaysi saytlarga kirayotgani ekranda chiqariladi

  6. Dastur to'xtatilishi (Ctrl+C)
     └─ ARP jadvallar avtomatik qaytariladi (restore)
     └─ Statistika ko'rsatiladi

🎯 MISOL:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

$ sudo python3 arp_dns_sniffer.py

🔧 TARMOQ INTERFEYSINI TANLANG
════════════════════════════════════════════════════════════════

📋 Mavjud interfeyslar:
  1. wlan0
  2. eth0
  3. docker0

🖱️  Raqamni tanlang (1-3): 1

✅ Tanlangan interfeys: wlan0
   MAC manzili: aa:bb:cc:dd:ee:ff

🔍 TARMOQ SKANERLASHI BOSHLANMOQDA
════════════════════════════════════════════════════════════════

📡 Skanerlanyotgan tarmoq: 192.168.1.0/24
📍 Mahalliy IP: 192.168.1.100
🔄 Skanerlash davom etmoqda...

✅ 192.168.1.1    | 00:11:22:33:44:55
✅ 192.168.1.50   | aa:bb:cc:dd:ee:01
✅ 192.168.1.75   | aa:bb:cc:dd:ee:02
✅ 192.168.1.99   | aa:bb:cc:dd:ee:03

📊 Jami qurilmalar: 4

🎯 NISHON QURILMANI TANLANG
════════════════════════════════════════════════════════════════

📍 Gateway IP: 192.168.1.1

📋 Mavjud qurilmalar:
  1. 192.168.1.50   | aa:bb:cc:dd:ee:01
  2. 192.168.1.75   | aa:bb:cc:dd:ee:02
  3. 192.168.1.99   | aa:bb:cc:dd:ee:03

🖱️  Raqamni tanlang (1-3): 1

✅ Nishon tanlandi:
   IP: 192.168.1.50
   MAC: aa:bb:cc:dd:ee:01
   Gateway IP: 192.168.1.1
   Gateway MAC: 00:11:22:33:44:55

🚀 ARP SPOOFING JARAYONI BOSHLANMOQDA
════════════════════════════════════════════════════════════════

📊 DNS SNIFFING BOSHLANMOQDA
════════════════════════════════════════════════════════════════

🌐 Nishon qurilmadan keladigan DNS so'rovlari:

🌐 [14:25:33] DNS so'rovi: google.com
🌐 [14:25:35] DNS so'rovi: youtube.com
🌐 [14:25:37] DNS so'rovi: facebook.com
🌐 [14:25:40] DNS so'rovi: instagram.com
🌐 [14:25:42] DNS so'rovi: twitter.com

⚙️ MOSLAMALAR:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

• ARP paketlari har 1 soniyada yuboriladi
• DNS so'rovlari real vaqtda sniffer qilinadi
• Barcha xatoliklar avtomatik boshqariladi
• Verbose va warning xabarlari o'chirilgan

⚠️  MUHIM OGOHLANTIRISH:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔴 BU DASTUR FAQAT:
   • O'zingizning tarmoq infrastukturasingizda
   • Qonuniy va etik maqsadlarda
   • Testlash va o'rganish uchun ishlatilishi kerak

⚠️  BU DASTURNING YOMON MAQSADLARDA ISHLATILISHI:
   • Qonunsiz
   • Xavfli
   • Etik jihatdan noto'g'ri
   • Bir-biriga zarar beruvchi

💡 FOYDALANISH VARIANTLARI:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✓ Tarmoq xavfsizligini tekshirish
✓ Penetration testing
✓ Tarmoq diagnostika
✓ Educatsional maqsadlarda
✓ Cybersecurity o'rganish

❌ ISHLATMASLIGI KERAK:
✗ Boshqa odamlarning qurilmalarini hujumqa
✗ Malicious aktivlik
✗ Qonunsiz monitoringga
✗ Intellektual mulklarni o'g'irlanishiga

📚 KUTUBXONALAR:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Scapy - Paket olish-yuborish kutubxonasi
   https://scapy.readthedocs.io/

Python Documentation
   https://docs.python.org/3/

🔧 TUZATISH VA XATOLAR:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

❌ "PermissionError: Operation not permitted"
   ✓ Sudo bilan ishga tushirish: sudo python3 arp_dns_sniffer.py

❌ "ModuleNotFoundError: No module named 'scapy'"
   ✓ Scapyni o'rnatish: pip install scapy

❌ "Interface not found"
   ✓ Interfeysingizni tekshirish: ifconfig yoki ipconfig

❌ "No packet captured"
   ✓ Tarmoqdagi qurilmalar faol ekanligini tekshiring
   ✓ Firewall sozlamalarini tekshiring

📞 QALVA/FEEDBACK:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Agar qalvalar bo'lsa:
   1. IPv4 va IPv6 sozlamalarini tekshiring
   2. Firewall qoidalarini o'zgartirib ko'ring
   3. Boshqa ARP spoofing dasturlarini o'chiring
   4. Interfeys to'g'ri tanlanganligi tekshiring

═══════════════════════════════════════════════════════════════════════════════
                           ✅ TAYYOR! ISHGA TUSHIRING!
═══════════════════════════════════════════════════════════════════════════════
"""
    
    print(instructions)


if __name__ == "__main__":
    print("\n" + "="*70)
    print("🛡️  ARP SPOOFING VA DNS SNIFFER - SETUP")
    print("="*70)
    
    # Kutubxonalarni o'rnatish
    install_dependencies()
    
    # Ko'rsatmalari chiqarish
    print_instructions()
    
    print("\n✅ Barcha narsalar tayyor! Dasturni ishga tushirishingiz mumkin:")
    print(f"   $ sudo python3 arp_dns_sniffer.py\n")
