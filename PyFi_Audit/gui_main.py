# gui_main.py
import customtkinter as ctk
from tkinter import filedialog, messagebox, ttk
import threading
import queue
import subprocess
import re
import time

from utils import network_utils
from attacks import dictionary_attack, wps_bruteforce # y los demás
from deauth import deauthenticate

# Configuración de la apariencia
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class PyFiAuditApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("PyFi_Audit - Herramienta de Auditoría WiFi")
        self.geometry("800x600")

        # Cola para comunicación entre hilos
        self.queue = queue.Queue()

        # Pestañas
        self.tab_view = ctk.CTkTabview(self)
        self.tab_view.pack(expand=True, fill="both", padx=10, pady=10)

        self.scanner_tab = self.tab_view.add("Escaner")
        self.attack_tab = self.tab_view.add("Ataques")
        self.deauth_tab = self.tab_view.add("Desautenticación")
        
        # --- Pestaña de Escaner ---
        self.setup_scanner_tab()
        
        # --- Pestaña de Ataques ---
        self.setup_attack_tab()

        # --- Pestaña de Desautenticación ---
        self.setup_deauth_tab()

        # Iniciar el procesamiento de la cola
        self.process_queue()

    def setup_scanner_tab(self):
        # ... (código para widgets de la pestaña de escaner)
        # Interfaz de red
        self.iface_label = ctk.CTkLabel(self.scanner_tab, text="Interfaz de Red:")
        self.iface_label.pack(pady=(10,0))
        self.iface_entry = ctk.CTkEntry(self.scanner_tab, placeholder_text="Ej: wlan0")
        self.iface_entry.pack()

        self.scan_button = ctk.CTkButton(self.scanner_tab, text="Escanear Redes", command=self.start_scan_thread)
        self.scan_button.pack(pady=10)

        # Tabla para mostrar redes
        columns = ("SSID", "BSSID", "Canal", "Cifrado")
        self.tree = ttk.Treeview(self.scanner_tab, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
        self.tree.pack(expand=True, fill="both", padx=10, pady=10)

    def setup_attack_tab(self):
        # ... (código para widgets de la pestaña de ataques)
        self.attack_type = ctk.CTkComboBox(self.attack_tab, values=["Diccionario WPA/WPA2", "Fuerza Bruta WPS"])
        self.attack_type.pack(pady=10)
        
        self.target_bssid_label = ctk.CTkLabel(self.attack_tab, text="BSSID Objetivo:")
        self.target_bssid_label.pack()
        self.target_bssid_entry = ctk.CTkEntry(self.attack_tab, placeholder_text="Autocompletado desde escaner")
        self.target_bssid_entry.pack()

        self.wordlist_button = ctk.CTkButton(self.attack_tab, text="Seleccionar Diccionario", command=self.select_wordlist)
        self.wordlist_button.pack(pady=10)
        self.wordlist_path_label = ctk.CTkLabel(self.attack_tab, text="Ningún archivo seleccionado")
        self.wordlist_path_label.pack()
        
        self.start_attack_button = ctk.CTkButton(self.attack_tab, text="Iniciar Ataque", command=self.start_attack_thread, fg_color="red")
        self.start_attack_button.pack(pady=20)
        
        # Feedback del ataque
        self.progress_bar = ctk.CTkProgressBar(self.attack_tab)
        self.progress_bar.pack(fill="x", padx=20)
        self.progress_bar.set(0)

        self.eta_label = ctk.CTkLabel(self.attack_tab, text="Tiempo restante: --:--:--")
        self.eta_label.pack()
        
        self.output_console = ctk.CTkTextbox(self.attack_tab, height=200)
        self.output_console.pack(expand=True, fill="both", padx=10, pady=10)
        
    def setup_deauth_tab(self):
        # ... (código para widgets de la pestaña de desautenticación)
        pass # Similar a los otros

    def select_wordlist(self):
        self.wordlist_path = filedialog.askopenfilename(title="Selecciona un diccionario", filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
        if self.wordlist_path:
            self.wordlist_path_label.configure(text=os.path.basename(self.wordlist_path))
            
    def start_scan_thread(self):
        iface = self.iface_entry.get()
        if not iface:
            messagebox.showerror("Error", "Debes especificar una interfaz de red.")
            return
        
        # Limpiar tabla anterior
        for i in self.tree.get_children():
            self.tree.delete(i)
            
        # Ejecutar en un hilo para no bloquear la GUI
        threading.Thread(target=network_utils.scan_networks, args=(iface, self.queue), daemon=True).start()

    def start_attack_thread(self):
        # ... Lógica para obtener los parámetros y empezar el hilo de ataque
        bssid = self.target_bssid_entry.get()
        attack = self.attack_type.get()
        iface = self.iface_entry.get()

        if attack == "Diccionario WPA/WPA2":
             if not hasattr(self, 'wordlist_path') or not self.wordlist_path:
                 messagebox.showerror("Error", "Debes seleccionar un archivo de diccionario.")
                 return
             threading.Thread(target=dictionary_attack.attack, args=(iface, bssid, self.wordlist_path, self.queue), daemon=True).start()
        # elif ... otros ataques

    def process_queue(self):
        try:
            message = self.queue.get_nowait()
            # Actualizar la GUI basado en el mensaje
            if message.startswith("SCAN_RESULT:"):
                data = message.replace("SCAN_RESULT:", "").split(',')
                self.tree.insert("", "end", values=data)
            elif message.startswith("LOG:"):
                self.output_console.insert("end", message.replace("LOG:", "") + "\n")
            elif message.startswith("PROGRESS:"):
                progress = float(message.split(':')[1])
                self.progress_bar.set(progress)
            elif message.startswith("ETA:"):
                self.eta_label.configure(text=f"Tiempo restante: {message.split(':')[1]}")
            elif message.startswith("SUCCESS:"):
                self.output_console.insert("end", f"\n!!! ÉXITO !!!\n{message.replace('SUCCESS:', '')}\n")
                messagebox.showinfo("Éxito", f"¡Ataque completado!\n{message.replace('SUCCESS:', '')}")

        except queue.Empty:
            pass
        finally:
            # Volver a llamar a esta función después de 100ms
            self.after(100, self.process_queue)

if __name__ == "__main__":
    app = PyFiAuditApp()
    app.mainloop()