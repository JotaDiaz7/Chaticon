import json
from flask import Flask, jsonify, request, send_file 
from flask_cors import CORS  
import pandas as pd  
# Example: reuse your existing OpenAI setup
from openai import OpenAI

from emojis import modelo_emojis, traducir_a_emojis
from tiempo import obtener_datos_tiempo, generar_grafico_tiempo
from traductor import traducir_a_ingles, traducir_a_espanol


app = Flask(__name__)
CORS(app)  

# Ruta para traducir un texto a emojis
@app.route('/emojis', methods=['GET'])
def traducir_texto_a_emojis():
    texto = request.args.get('texto')
    if not texto:
        return jsonify({"error": "No se ha proporcionado ningún texto"}), 400

    emojis = traducir_a_emojis(modelo_emojis, texto)  
    return jsonify(emojis)  

# Ruta para obtener el tiempo
@app.route('/tiempo', methods=['GET'])
def obtener_tiempo_info():
    ciudad = request.args.get('ciudad')
    if not ciudad:
        return jsonify({"error": "No se ha especificado ninguna ciudad"}), 400 

    datos = obtener_datos_tiempo(ciudad)

    temperaturas = [item['main']['temp'] for item in datos['list']]
    humedades = [item['main']['humidity'] for item in datos['list']]
    presiones = [item['main']['pressure'] for item in datos['list']]
    velocidades_viento = [item['wind']['speed'] for item in datos['list']]
    descripciones = [item['weather'][0]['description'] for item in datos['list']]

    df_temperatura = pd.DataFrame(temperaturas, columns=['Temperatura'])
    df_humedad = pd.DataFrame(humedades, columns=['Humedad'])
    df_presion = pd.DataFrame(presiones, columns=['Presión'])
    df_viento = pd.DataFrame(velocidades_viento, columns=['Viento'])

    estadisticas = {
        "media_temperatura": df_temperatura['Temperatura'].mean(),
        "max_temperatura": df_temperatura['Temperatura'].max(),
        "min_temperatura": df_temperatura['Temperatura'].min(),
        "media_humedad": df_humedad['Humedad'].mean(),
        "media_presion": df_presion['Presión'].mean(),
        "media_viento": df_viento['Viento'].mean(),
        "descripciones": descripciones
    }

    return jsonify(estadisticas)  

# Ruta para obtener un gráfico del tiempo en una ciudad específica
@app.route('/tiempo/grafica', methods=['GET'])
def obtener_grafica_tiempo():
    ciudad = request.args.get('ciudad')
    if not ciudad:
        return jsonify({"error": "No se ha especificado ninguna ciudad"}), 400

    datos = obtener_datos_tiempo(ciudad)
    if datos:
        img = generar_grafico_tiempo(datos, ciudad)  
        return send_file(img, mimetype='image/png')  
    else:
        return jsonify({"error": "Datos de tiempo no disponibles"}), 404 
    
# Ruta para traducir un texto al inglés
@app.route('/traductor', methods=['GET'])
def traducir_texto_a_ingles():
    texto = request.args.get('texto')
    lang = request.args.get('lang')

    if not texto:
        return jsonify({"error": "No se ha proporcionado ningún texto"}), 400

    if lang == 'ESP':
        traduccion = traducir_a_espanol(texto)
    elif lang == 'ENG':
        traduccion = traducir_a_ingles(texto)
    else:
        return jsonify({"error": "Idioma no soportado"}), 400

    return jsonify({"traduccion": traduccion})

@app.route("/chat", methods=['GET'])
def data_chat():
    # Point to the local server
    client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")
    texto = request.args.get('texto')

    completion = client.chat.completions.create(

        model="model-identifier",

        messages=[
            {"role": "system", "content": "Eres una persona, te llamas Joana, hablas español y das respuestas cortas"},
            {"role": "user", "content": texto}
        ],

        temperature=0.5,#0 muy científico
    )

    print(completion.choices[0].message.content)
    return jsonify({"respuesta":completion.choices[0].message.content})

if __name__ == "__main__":
    app.run(port=5000)
