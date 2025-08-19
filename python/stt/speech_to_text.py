import sounddevice as sd
import numpy as np
import queue
from faster_whisper import WhisperModel

q = queue.Queue()
model = WhisperModel("base", device="cpu", compute_type="int8")

def callback(indata, frames, time, status):
    q.put(indata.copy())

with sd.InputStream(samplerate=16000, channels=1, callback=callback):
    print("Listening... Press Ctrl+C to stop.")
    audio_buffer = np.empty((0,), dtype=np.float32)

    try:
        while True:
            audio_chunk = q.get().flatten()
            audio_buffer = np.concatenate((audio_buffer, audio_chunk))

            if len(audio_buffer) > 16000 * 5:  # process every 5 seconds
                segments, _ = model.transcribe(audio_buffer)
                for seg in segments:
                    print(seg.text, end="", flush=True)
                audio_buffer = np.empty((0,), dtype=np.float32)

    except KeyboardInterrupt:
        print("\nStopped.")

