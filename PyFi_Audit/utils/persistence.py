# utils/persistence.py
import pickle
import os

def save_state(state, filename):
    with open(filename, 'wb') as f:
        pickle.dump(state, f)
    print(f"Estado del ataque guardado en: {filename}")

def load_state(filename):
    if os.path.exists(filename):
        with open(filename, 'rb') as f:
            return pickle.load(f)
    else:
        print(f"Error: No se encontró el archivo de sesión {filename}")
        return None