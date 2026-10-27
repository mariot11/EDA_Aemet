import os
import sys
import time
import requests
import json
import zipfile
import pandas as pd

print(sys.executable)
from dotenv import load_dotenv

load_dotenv()  # Carga las variables del fichero .env como variables de entorno

api_key = os.getenv("PAISES_API_KEY")  # None si la variable no existe
url = "https://api.restcountries.com/countries/v5"
limite = 30
offset = 0
paises = []

if not api_key:
  print("Error: No se ha encontrado la API key en el fichero .env")
  sys.exit()  # Detiene el script de forma limpia

mis_headers = {"Authorization" : f"Bearer {api_key}"}
continuar = True

while continuar:
    params = {"region" : "Europe", "limit" : limite,
               "offset" : offset}

    try:
        response = requests.get(url, params=params, headers=mis_headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        paises.extend(data["data"]["objects"])
        continuar = data["data"]["meta"]["more"]
    except requests.exceptions.Timeout:
        print("El servidor ha tardado demasiado en responder")
    except requests.exceptions.HTTPError as e:
        print("Error HTTP:", e)
    except requests.exceptions.RequestException as e:
        print("Error en la solicitud:", e)

    offset += limite
    time.sleep(1)

nombre_archivo = "data/paises_europa.json"

with open(nombre_archivo, "w", encoding="utf-8") as archivo:
  json.dump(paises, archivo, ensure_ascii=False, indent=4)

print(f"¡Fichero '{nombre_archivo}' generado y guardado con éxito!")