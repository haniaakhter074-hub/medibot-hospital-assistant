# MediBot – Hospital Virtual Assistant (Python)

## Setup
    pip install -r requirements.txt
    streamlit run app.py

## Optional: full AI answers (Claude)
    # Windows (PowerShell)
    setx ANTHROPIC_API_KEY "your-key"
    # macOS/Linux
    export ANTHROPIC_API_KEY="your-key"
Without a key the app still works using the built-in symptom engine.

## Files
- app.py      – Streamlit interface (7 tabs)
- engine.py   – emergency detection, symptom checker, tips, AI reply
- geo.py      – nearby hospital search (built-in list + live OpenStreetMap)
- voice.py    – voice input (SpeechRecognition) and voice reply (gTTS)
- storage.py  – SQLite: chat log, reminders, appointments
- i18n.py     – English + Urdu text (add more languages here)

## Before real hospital use
Verify emergency numbers, replace sample facilities in geo.py, and get
clinical review. This is a student/prototype project, not a medical device.
