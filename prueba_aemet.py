import requests

url = "https://opendata.aemet.es/opendata/api/datos/anexos/metadatos"

try:
  print("Intentando conectar con AEMET...")
  response = requests.get(url, timeout=10)
  print(f"¡Conexión exitosa! Código HTTP: {response.status_code}")
except requests.exceptions.Timeout:
  print("Error: La conexión ha caducado (Timeout).")
except Exception as e:
  print(f"Ha ocurrido un error: {e}")