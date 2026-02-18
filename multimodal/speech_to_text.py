import whisper
import tempfile

model = whisper.load_model("base")

def speech_to_text(audio_bytes: bytes) -> str:
    # Do NOT force .wav
    with tempfile.NamedTemporaryFile(delete=True) as tmp:
        tmp.write(audio_bytes)
        tmp.flush()

        result = model.transcribe(tmp.name)

    return result.get("text", "").strip()
