from transformers import TFMarianMTModel, MarianTokenizer

# Modelos de traducción
model_name_es_en = 'Helsinki-NLP/opus-mt-es-en'
model_es_en = TFMarianMTModel.from_pretrained(model_name_es_en)
tokenizer_es_en = MarianTokenizer.from_pretrained(model_name_es_en)

model_name_en_es = 'Helsinki-NLP/opus-mt-en-es'
model_en_es = TFMarianMTModel.from_pretrained(model_name_en_es)
tokenizer_en_es = MarianTokenizer.from_pretrained(model_name_en_es)

def traducir_a_ingles(texto):
    inputs = tokenizer_es_en(texto, return_tensors="tf", padding=True)
    translated = model_es_en.generate(**inputs)
    traduccion = tokenizer_es_en.batch_decode(translated, skip_special_tokens=True)[0]
    return traduccion

def traducir_a_espanol(texto):
    inputs = tokenizer_en_es(texto, return_tensors="tf", padding=True)
    translated = model_en_es.generate(**inputs)
    traduccion = tokenizer_en_es.batch_decode(translated, skip_special_tokens=True)[0]
    return traduccion