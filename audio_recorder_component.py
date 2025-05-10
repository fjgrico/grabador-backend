import streamlit as st
import streamlit.components.v1 as components

def audio_recorder():
    audio_recorder_html = """
    <script>
    let mediaRecorder;
    let audioChunks = [];

    async function startRecording() {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream);
        mediaRecorder.start();
        audioChunks = [];

        mediaRecorder.addEventListener("dataavailable", event => {
            audioChunks.push(event.data);
        });

        mediaRecorder.addEventListener("stop", () => {
            const audioBlob = new Blob(audioChunks);
            const reader = new FileReader();
            reader.readAsDataURL(audioBlob);
            reader.onloadend = () => {
                const base64AudioMessage = reader.result.split(',')[1];
                const streamlitAudio = window.parent.streamlit;
                streamlitAudio.setComponentValue(base64AudioMessage);
            };
        });
    }

    function stopRecording() {
        mediaRecorder.stop();
    }
    </script>

    <button onclick="startRecording()">🎙️ Empezar</button>
    <button onclick="stopRecording()">⏹️ Detener</button>
    """

    return components.html(audio_recorder_html, height=120)
