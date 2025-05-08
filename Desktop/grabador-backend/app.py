from flask import Flask, request, jsonify
import whisper
import tempfile

app = Flask(__name__)
model = whisper.load_model("base")  # Puedes cambiar a 'small', 'medium', etc.

@app.route("/transcribir", methods=["POST"])
def transcribir_audio():
    if "audio" not in request.files:
        return jsonify({"error": "No se envió audio"}), 400

    audio = request.files["audio"]
    with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as tmp:
        audio.save(tmp.name)
        result = model.transcribe(tmp.name)
        return jsonify({"transcripcion": result["text"]})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
