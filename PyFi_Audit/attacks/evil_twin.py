# attacks/evil_twin.py
import os

def attack(interface, ssid):
    print(f"Creando un Evil Twin con SSID: {ssid}")
    # 1. Configurar hostapd para crear el AP falso
    # 2. Configurar un servidor DHCP para asignar IPs a los clientes
    # 3. Utilizar un sniffer (como Wireshark o Scapy) para capturar el tráfico
    #    de los clientes que se conecten.