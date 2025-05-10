from gtts import gTTS
import os
from datetime import datetime

def reproducir_texto_en_audio(texto):
    try:
        nombre_archivo = f"interpretacion_{datetime.now().strftime('%Y%m%d%H%M%S')}.mp3"
        tts = gTTS(text=texto, lang="es")
        tts.save(nombre_archivo)
        return nombre_archivo
    except Exception as e:
        print(f"❌ Error al generar audio: {e}")
        return None
