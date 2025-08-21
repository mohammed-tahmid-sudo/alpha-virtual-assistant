import sys
from gtts import gTTS
import os

if len(sys.argv) < 2:
    print("Usage: python tts_gtts.py 'Your text here'")
    sys.exit(1)

text = " ".join(sys.argv[1:])
tts = gTTS(text=text, lang='en')
tts.save("output.mp3")

# Play the audio (Linux example)
os.system("mpv output.mp3")  # or "mpg321" depending on your system

