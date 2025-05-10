# ✅ Suenia - app.py con grabación real vía streamlit-audiorecorder
import streamlit as st
import requests
import tempfile
import base64
from streamlit_audiorecorder import audiorecorder
from utils_gpt import interpretar_sueno
from utils_audio import reproducir_texto_en_audio

st.set_page_config(page_title="💤 Suenia | Interpretación de Sueños", layout="centered")

st.markdown("<h1 style='text-align: center;'>💤 Suenia | Interpretación de Sueños</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Describe aquí tu sueño si no vas a grabarlo...</p>", unsafe_allow_html=True)

# Entrada manual
sueno_texto = st.text_input("✍️ Escribe tu sueño aquí...")

# Grabador de audio real
st.markdown("## 🎙️ O graba tu sueño con tu voz:")
audio_data = audiorecorder("🎤 Iniciar grabación", "⏹️ Detener grabación")

# Mostrar checkbox si hay audio válido
usar_audio = False
if isinstance(audio_data, bytes) and len(audio_data) > 10000:
    usar_audio = st.checkbox("Usar grabación de voz en lugar del texto escrito")

# Acción principal
if st.button("Interpretar mi sueño"):
    if usar_audio:
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
                f.write(audio_data)
                audio_path = f.name

            files = {'audio': open(audio_path, 'rb')}
            response = requests.post("https://grabador-backend.onrender.com/transcribir", files=files)
            response.raise_for_status()
            transcripcion = response.json().get("transcripcion", "").strip()

            if not transcripcion:
                st.warning("No se pudo transcribir el audio.")
                st.stop()

            st.markdown("### 📝 Transcripción del sueño:")
            st.text_area("Texto transcrito:", value=transcripcion, height=160)
            sueno_procesar = transcripcion

        except Exception as e:
            st.error(f"❌ Error al enviar el audio: {str(e)}")
            st.stop()

    elif sueno_texto.strip():
        sueno_procesar = sueno_texto.strip()
    else:
        st.warning("Por favor, escribe o graba un sueño.")
        st.stop()

    # Interpretación con GPT
    interpretacion = interpretar_sueno(sueno_procesar)
    st.markdown("### 🔮 Interpretación del Sueño:")
    st.write(interpretacion)

    if st.checkbox("🔊 Escuchar interpretación en voz"):
        audio_file = reproducir_texto_en_audio(interpretacion)
        if audio_file:
            st.audio(audio_file)
