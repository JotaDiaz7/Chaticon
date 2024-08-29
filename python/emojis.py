import pandas as pd
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from nltk.tokenize import word_tokenize

nltk.download('punkt')
nltk.download('stopwords')

stemmer = SnowballStemmer('spanish')

def preprocesar_texto(texto):
    texto = re.sub(r'\W', ' ', texto)
    texto = texto.lower()
    tokens = word_tokenize(texto)
    tokens = [stemmer.stem(token) for token in tokens if token not in stopwords.words('spanish')]
    return ' '.join(tokens)  

def entrenar_modelo(csv_path):
    # Cargar datos de entrenamiento desde el CSV
    df = pd.read_csv(csv_path)

    # Filtrar las filas con emojis duplicados
    df = df.drop_duplicates(subset='emojis')

    # Preprocesar las palabras clave en el conjunto de datos
    df['palabras'] = df['palabras'].apply(preprocesar_texto)

    # Vectorizar las palabras clave usando TF-IDF
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(df['palabras'])

    # Entrenar el modelo Naive Bayes
    modelo = MultinomialNB().fit(X, df['emojis'])

    return {
        'modelo': modelo,
        'vectorizer': vectorizer
    }

def traducir_a_emojis(modelo_emojis, texto, num_emojis=5):
    texto = preprocesar_texto(texto)

    modelo = modelo_emojis['modelo']
    vectorizer = modelo_emojis['vectorizer']

    X_test = vectorizer.transform([texto])

    probabilidades = modelo.predict_proba(X_test)[0]

    indices_ordenados = probabilidades.argsort()[::-1][:num_emojis]

    resultado = []
    for idx in indices_ordenados:
        emoji = modelo.classes_[idx]
        similitud = round(probabilidades[idx] * 100, 2)
        resultado.append({"emojis": emoji, "similitud": similitud})

    return resultado

modelo_emojis = entrenar_modelo('csv/emojis.csv')
