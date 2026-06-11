import io

from gtts import gTTS


def generate_audio(text):

    if not text.strip():
        return None

    tts = gTTS(
        text=text,
        lang="en",
        slow=False
    )

    audio_buffer = io.BytesIO()

    tts.write_to_fp(audio_buffer)

    audio_buffer.seek(0)

    return audio_buffer