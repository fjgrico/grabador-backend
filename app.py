from flask import Flask, request, jsonify
import tempfile
import subprocess
import os

app = Flask(__name__)

@app.route("/transcribir", methods=["POST"])
def transcribir_audio():
    if "audio" not in request.files:
        return jsonify({"error": "No se envió audio"}), 400

    audio = request.files["audio"]
    with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as tmp:
        audio.save(tmp.name)
        input_path = tmp.name
        output_path = input_path + ".txt"

        try:
            # Convierte a WAV con ffmpeg
            wav_path = input_path.replace(".webm", ".wav")
            subprocess.run(["ffmpeg", "-y", "-i", input_path, wav_path], check=True)

            # Ejecuta whisper.cpp usando el modelo multilingüe
            subprocess.run([
                "./main",
                "-m", "models/ggml-tiny.bin",
                "-f", wav_path,
                "-otxt"
            ], check=True)

            # Lee la salida de texto generada
            with open(wav_path + ".txt", "r") as f:
                texto = f.read()

            return jsonify({"transcripcion": texto.strip()})

        except Exception as e:
            return jsonify({"error": f"Error al transcribir: {str(e)}"}), 500

        finally:
            os.remove(input_path)
            if os.path.exists(wav_path):
                os.remove(wav_path)
            if os.path.exists(wav_path + ".txt"):
                os.remove(wav_path + ".txt")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
