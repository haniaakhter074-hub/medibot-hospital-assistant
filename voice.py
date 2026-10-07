"""Voice helpers - Python only.

transcribe(): WAV bytes -> text using the SpeechRecognition package
              (Google's free web recognizer, needs internet).
speak():      text -> MP3 bytes using gTTS (needs internet). Optional.
"""
import io
import re


def transcribe(wav_bytes: bytes, language_code: str):
    """Return (text, error). Exactly one of them is None."""
    try:
        import speech_recognition as sr
    except ImportError:
        return None, "SpeechRecognition not installed (pip install SpeechRecognition)"
    rec = sr.Recognizer()
    try:
        with sr.AudioFile(io.BytesIO(wav_bytes)) as src:
            audio = rec.record(src)
        text = rec.recognize_google(audio, language=language_code)
        return text, None
    except sr.UnknownValueError:
        return None, "unclear"
    except sr.RequestError as e:
        return None, f"service error: {e}"
    except Exception as e:  # unreadable audio etc.
        return None, f"{type(e).__name__}: {e}"


def _clean_for_speech(text: str) -> str:
    text = re.sub(r"[*_`#>]", "", text)
    text = re.sub(r"[\U0001F300-\U0001FAFF\u2600-\u27BF]", "", text)  # emojis
    return text.strip()[:900]


def speak(text: str, tts_lang: str):
    """Return MP3 bytes or None."""
    try:
        from gtts import gTTS
        buf = io.BytesIO()
        gTTS(_clean_for_speech(text), lang=tts_lang).write_to_fp(buf)
        return buf.getvalue()
    except Exception:
        return None
