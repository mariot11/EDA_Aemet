import os
import sys
import time
import requests
import json
import pandas as pd

print(sys.executable)
from dotenv import load_dotenv

load_dotenv()  # Carga las variables del fichero .env como variables de entorno

# Url base con los endpoints principales
AEMET_BASE_URL = "https://opendata.aemet.es/opendata/api/valores/climatologicos/mensualesanuales/datos"

api_key = os.getenv("AEMET_API_KEY")  # None si la variable no existe
anio_inicial = 2021
anio_limite = 2025
estacion = "8416"
datos = []

def obtener_clima_mensual_valencia(anio_ini: int, anio_fin: int, idema: str = "8416") -> list:
    """
    Obtiene los valores climatológicos mensuales/anuales uniendo la base y los parámetros.
    """
    # 2. Juntamos las piezas (base + parámetros dinámicos) usando f-strings de Python
    url_endpoint = f"{AEMET_BASE_URL}/anioini/{anio_ini}/aniofin/{anio_fin}/estacion/{idema}"
    
    print(f"Consultando URL: {url_endpoint}")
    #return obtener_datos_aemet(url_endpoint)
    return url_endpoint


if not api_key:
  print("Error: No se ha encontrado la API key en el fichero .env")
  sys.exit()  # Detiene el script de forma limpia

mis_headers = {"api_key" : f"{api_key}"}
continuar = True

for anio in range(anio_inicial, anio_limite +1):
    url = obtener_clima_mensual_valencia(anio, anio, estacion)

    try:
        response = requests.get(url, headers=mis_headers, timeout=10)
        response.raise_for_status()
        resultado_json = response.json()
        url_descarga = resultado_json.get("datos")

        if not url_descarga:
            print(f"No se encontró URL de descarga para el año {anio}.")
            continue

        # Segunda petición a la URL temporal (sin headers) para bajar el JSON real
        response_datos = requests.get(url_descarga, timeout=15)
        response_datos.raise_for_status()
        registros_anuales = response_datos.json()
        
        datos.extend(registros_anuales)
        print(f"-> Año {anio} descargado con éxito ({len(registros_anuales)} registros).")

    except requests.exceptions.Timeout:
        print("El servidor ha tardado demasiado en responder")
    except requests.exceptions.HTTPError as e:
        print("Error HTTP:", e)
    except requests.exceptions.RequestException as e:
        print("Error en la solicitud:", e)

    time.sleep(1)

os.makedirs("data", exist_ok=True)
nombre_archivo = "data/datos_climatologicos_valencia.json"

with open(nombre_archivo, "w", encoding="utf-8") as archivo:
  json.dump(datos, archivo, ensure_ascii=False, indent=4)

print(f"¡Fichero '{nombre_archivo}' generado y guardado con éxito! Total de registros: {len(datos)}")