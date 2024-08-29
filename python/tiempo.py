import requests
from datetime import datetime
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from io import BytesIO

API_KEY_OPENWEATHER = '87ab7953898870a359d3d75a97fc2b5e'

def obtener_datos_tiempo(ciudad):
    url = f"http://api.openweathermap.org/data/2.5/forecast?lang=es&units=metric&appid={API_KEY_OPENWEATHER}&q={ciudad}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None

def generar_grafico_tiempo(datos, ciudad):
    fechas = []
    temperaturas = []

    for item in datos['list']:
        fecha_obj = datetime.strptime(item['dt_txt'], '%Y-%m-%d %H:%M:%S')
        fecha_formateada = fecha_obj.strftime('%d %b %H:%M')
        fechas.append(fecha_formateada)
        temperaturas.append(item['main']['temp'])

    plt.figure(figsize=(10, 6.5))
    plt.plot(fechas, temperaturas, marker='o', linestyle='-', color='b')
    plt.title(f'Temperaturas previstas para {ciudad}', fontsize=16)
    plt.xlabel("Fecha y Hora", fontsize=14)
    plt.ylabel("Temperaturas (°C)", fontsize=14)
    plt.xticks(rotation=45, ha='right')
    plt.grid(True)
    plt.tight_layout()

    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close('all')

    return img
