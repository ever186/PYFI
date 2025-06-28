# utils/scanner.py
from scapy.all import *

def scan_networks(interface):
    print("Escaneando redes...")
    # Lógica con Scapy para escanear y mostrar redes WIFI
    # Se pueden mostrar BSSID, SSID, Canal, Cifrado, etc.