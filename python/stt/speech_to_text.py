# pip install faster-whisper sounddevice webrtcvad numpy

import sounddevice as sd
import numpy as np
import webrtcvad, collections, time
from faster_whisper import WhisperModel
import warnings, os

warnings.filterwarnings("ignore")  # hide Python warnings
os.environ["CT2_VERBOSE"] = "0"  # hide faster-whisper warnings

SAMPLE_RATE = 16000
FRAME_DURATION = 30  # ms
FRAME_SIZE = int(SAMPLE_RATE * FRAME_DURATION / 1000)

vad = webrtcvad.Vad(2)  # 0-3, higher = more aggressive
model = WhisperModel("small", device="cpu")


def record_frames(timeout=2):
    """Yield audio frames until silence for 'timeout' seconds"""
    ring_buffer = collections.deque(maxlen=int(timeout * 1000 / FRAME_DURATION))
    last_speech = time.time()

    with sd.InputStream(
        channels=1, samplerate=SAMPLE_RATE, dtype="int16", blocksize=FRAME_SIZE
    ) as stream:
        while True:
            frame, _ = stream.read(FRAME_SIZE)
            frame_bytes = frame.tobytes()
            is_speech = vad.is_speech(frame_bytes, SAMPLE_RATE)

            if is_speech:
                last_speech = time.time()
                yield frame
            else:
                if time.time() - last_speech > timeout:
                    break


def transcribe():
    audio = b"".join([f.tobytes() for f in record_frames()])
    if not audio:
        return None

    audio_np = np.frombuffer(audio, np.int16).astype(np.float32) / 32768.0
    segments, _ = model.transcribe(audio_np, beam_size=5)

    text = " ".join([seg.text for seg in segments])
    return text.strip()


if __name__ == "__main__":
    print("Speak something... (program exits if you stop talking)")
    while True:
        text = transcribe()
        if text:
            print("You said:", text)
        else:
            print("No speech detected. Exiting.")
            break
