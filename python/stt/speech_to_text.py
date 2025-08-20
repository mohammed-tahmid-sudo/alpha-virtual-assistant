# run: pip install faster-whisper sounddevice soundfile numpy webrtcvad
from faster_whisper import WhisperModel
import sounddevice as sd
import numpy as np
import queue, threading, time
import webrtcvad

MODEL = "small"
DEVICE = "cpu"
SAMPLE_RATE = 16000
CHUNK_MS = 30            # 30ms frames
SILENCE_TIMEOUT = 4      # seconds to stop after silence

model = WhisperModel(MODEL, device=DEVICE, compute_type="int8" if DEVICE=="cpu" else "float16")
q = queue.Queue()
vad = webrtcvad.Vad(2)  # Aggressiveness 0-3
last_speech_time = time.time()

def audio_callback(indata, frames, time_info, status):
    if status: print("Audio status:", status)
    q.put(indata.copy())

def is_speech(frame):
    # frame must be 16-bit PCM mono
    pcm_data = (frame * 32768).astype(np.int16).tobytes()
    return vad.is_speech(pcm_data, SAMPLE_RATE)

def worker():
    global last_speech_time
    buf = np.zeros((0, 1), dtype=np.float32)
    while True:
        chunk = q.get()
        buf = np.concatenate([buf, chunk], axis=0)

        # process small frames for quick VAD
        while buf.shape[0] >= int(SAMPLE_RATE * (CHUNK_MS / 1000.0)):
            frame = buf[:int(SAMPLE_RATE * (CHUNK_MS / 1000.0)), 0]
            buf = buf[int(SAMPLE_RATE * (CHUNK_MS / 1000.0)):]
            
            if is_speech(frame):
                last_speech_time = time.time()
                # transcribe immediately
                segments, _ = model.transcribe(frame, language="en", vad_filter=True)
                for s in segments:
                    print(s.text)
            else:
                if time.time() - last_speech_time > SILENCE_TIMEOUT:
                    print("No speech detected. Stopping.")
                    return

threading.Thread(target=worker, daemon=True).start()
with sd.InputStream(channels=1, samplerate=SAMPLE_RATE, callback=audio_callback, blocksize=0):
    print("Listening… Speak something!")
    threading.Event().wait()

