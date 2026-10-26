import os
import sys

print(sys.executable)
from dotenv import load_dotenv

load_dotenv()  # Carga las variables del fichero .env como variables de entorno

api_key = os.getenv("AEMET_API_KEY")  # None si la variable no existe

# Comprueba que se ha cargado bien (no imprimas la clave entera si vas a compartir capturas)
if api_key:
  print("¡API Key cargada correctamente!")
else:
  print("Error: No se ha encontrado la API Key.")