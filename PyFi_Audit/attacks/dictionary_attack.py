# attacks/dictionary_attack.py
import subprocess
import os
import time

def get_wordlist_size(wordlist_path):
    with open(wordlist_path, 'r', errors='ignore') as f:
        return sum(1 for _ in f)

def attack(interface, bssid, wordlist, queue):
    # Poner la interfaz en modo monitor automáticamente
    queue.put("LOG:Poniendo la interfaz en modo monitor...")
    subprocess.run(['airmon-ng', 'start', interface], capture_output=True)
    monitor_interface = interface + "mon"

    # Iniciar captura de handshake
    queue.put(f"LOG:Iniciando captura de handshake para {bssid} en el canal X...")
    # Aquí iría el comando airodump-ng para capturar el handshake en un archivo .cap
    # ... (lógica para capturar handshake, por ejemplo, usando un subproceso airodump-ng
    # y enviando paquetes de desautenticación para acelerar el proceso)

    # Simulación de captura y crackeo
    queue.put("LOG:Handshake capturado: handshake-01.cap")
    queue.put("LOG:Iniciando crackeo con aircrack-ng...")
    
    total_passwords = get_wordlist_size(wordlist)
    start_time = time.time()

    # Usar aircrack-ng. Se lee su salida línea por línea.
    # El comando real sería algo como: ["aircrack-ng", "-w", wordlist, "-b", bssid, "handshake-01.cap"]
    # Aquí simulamos el proceso para demostrar el feedback:
    for i, password in enumerate(open(wordlist, 'r', errors='ignore')):
        time.sleep(0.01) # Simula el tiempo que toma probar una contraseña
        
        # Calcular progreso y ETA
        if i > 0:
            progress = (i + 1) / total_passwords
            elapsed_time = time.time() - start_time
            passwords_per_second = i / elapsed_time
            remaining_passwords = total_passwords - i
            
            if passwords_per_second > 0:
                eta_seconds = remaining_passwords / passwords_per_second
                eta_str = time.strftime('%H:%M:%S', time.gmtime(eta_seconds))
            else:
                eta_str = "Calculando..."

            # Enviar actualizaciones a la GUI cada 100 contraseñas
            if i % 100 == 0:
                queue.put(f"PROGRESS:{progress}")
                queue.put(f"ETA:{eta_str}")
                queue.put(f"LOG:Probando: {password.strip()}")

        # Simular que se encontró la contraseña
        if password.strip() == "password123":
            queue.put("PROGRESS:1.0")
            queue.put(f"SUCCESS:¡Contraseña encontrada!: {password.strip()}")
            return
            
    queue.put("LOG:Ataque finalizado. Contraseña no encontrada en el diccionario.")