# run: pip install faster-whisper sounddevice soundfile numpy
from faster_whisper import WhisperModel
import sounddevice as sd, soundfile as sf, numpy as np, queue, threading

MODEL = "small"               # small/medium for low-latency; large for accuracy
DEVICE = "cpu"               # or "cpu"
SAMPLE_RATE = 16000
CHUNK_SEC = 5                 # 1-5s chunk -> lower latency
model = WhisperModel(MODEL, device=DEVICE, compute_type="float16" if DEVICE=="cuda" else "int8")

q = queue.Queue()

def audio_callback(indata, frames, time, status):
    if status: print("Audio status:", status)
    q.put(indata.copy())

def worker():
    buf = np.zeros((0,1), dtype=np.float32)
    while True:
        chunk = q.get()
        buf = np.concatenate([buf, chunk], axis=0)
        if buf.shape[0] >= SAMPLE_RATE * CHUNK_SEC:
            piece = buf[:SAMPLE_RATE*CHUNK_SEC, 0]   # mono 1-D array
            buf = buf[SAMPLE_RATE*CHUNK_SEC:]
            # Option A: pass numpy array directly (must be mono float32 @16000)
            try:
                segments, info = model.transcribe(piece, language="en", vad_filter=True, condition_on_previous_text=False)
                for s in segments: print(s.text)
            except Exception as e:
                # fallback: write temp file and transcribe file path
                sf.write("tmp_chunk.wav", piece, SAMPLE_RATE)
                segments, info = model.transcribe("tmp_chunk.wav", vad_filter=True, condition_on_previous_text=False)
                for s in segments: print(s.text) 

# start threads + mic
threading.Thread(target=worker, daemon=True).start()
with sd.InputStream(channels=1, samplerate=SAMPLE_RATE, callback=audio_callback, blocksize=0):
    # print("Listening — Ctrl+C to stop")
    threading.Event().wait()

