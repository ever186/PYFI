# attacks/wps_bruteforce.py
import subprocess

def attack(interface, bssid):
    print(f"Iniciando ataque de fuerza bruta a WPS en {bssid}")
    # Utilizar Reaver para el ataque
    # subprocess.run(["reaver", "-i", interface, "-b", bssid, "-vv"])