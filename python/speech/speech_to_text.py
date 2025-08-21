import speech_recognition as sr
from faster_whisper import WhisperModel

# Initialize recognizer and Faster Whisper model
r = sr.Recognizer()
model = WhisperModel("small")  # small/medium/large
device = "cpu"  # or "cuda"

# Capture audio from microphone
with sr.Microphone() as source:
    print("Speak now...")
    audio = r.listen(source)

# Convert audio to WAV bytes
wav_data = audio.get_wav_data()

# Save audio to a temporary file
with open("temp.wav", "wb") as f:
    f.write(wav_data)

# Transcribe using Faster Whisper
segments, info = model.transcribe("temp.wav", beam_size=5)
for segment in segments:
    print(segment.text)

