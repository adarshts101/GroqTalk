import os
import base64
import requests

# ============ WELCOME TO GROQTALK ============
GROQ_API_KEY = "GROQ_API_KEY"  # 🔑 Replace with your actual Groq API key
AUDIO_FILE = "audio/test_audio.mp3"  # 🎧 Your audio input file
MODEL = "whisper-large-v3"           # 🧠 Whisper model name
# =============================================

def encode_audio_to_base64(audio_path):
    with open(audio_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")
    return encoded

def transcribe_audio(audio_path):
    print("🎙️ [GroqTalk] Encoding audio file...")
    encoded_audio = encode_audio_to_base64(audio_path)

    print("📡 [GroqTalk] Sending to Groq Whisper API...")
    url = "https://api.groq.com/openai/v1/audio/transcriptions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
    }
    files = {
        "file": (os.path.basename(audio_path), open(audio_path, "rb")),
        "model": (None, MODEL),
    }

    response = requests.post(url, headers=headers, files=files)

    if response.status_code == 200:
        print("✅ [GroqTalk] Transcription successful!")
        return response.json()["text"]
    else:
        print("❌ [GroqTalk] Error:", response.text)
        return None

if __name__ == "__main__":
    if not os.path.exists(AUDIO_FILE):
        print(f"⚠️ [GroqTalk] Audio file not found at {AUDIO_FILE}")
    else:
        transcript = transcribe_audio(AUDIO_FILE)
        if transcript:
            print("\n📝 TRANSCRIPTION RESULT:")
            print("----------------------------")
            print(transcript)
            print("----------------------------")
