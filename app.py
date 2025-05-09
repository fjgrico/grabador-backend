from flask import Flask, request, jsonify
import tempfile
import os
import openai

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/transcribir", methods=["POST"])
def transcribir_audio():
    if "audio" not in request.files:
        return jsonify({"error": "No se envió audio"}), 400

    audio = request.files["audio"]
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        audio.save(tmp.name)

        try:
            with open(tmp.name, "rb") as f:
                transcript = openai.Audio.transcribe("whisper-1", f)
                texto = transcript["text"]
        except Exception as e:
            return jsonify({"error": f"Error al transcribir: {str(e)}"}), 500
        finally:
            os.remove(tmp.name)

        return jsonify({"transcripcion": texto})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
