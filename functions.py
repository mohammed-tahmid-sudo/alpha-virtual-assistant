from gtts import gTTS
import sounddevice as sd
import speech_recognition as sr
import subprocess
import difflib
import speech_recognition as sr
from faster_whisper import WhisperModel
import os
import speech_recognition as sr
import numpy as np

class SpeechRecognizer:
    def __init__(self, model_size="small.en", sample_rate=16000, device=None, language="en", beam_size=2, cpu_threads=6):
        """
        Initialize the speech recognizer with Faster-Whisper.
        """
        self.model = WhisperModel(
            model_size,
            device="cpu",
            compute_type="int8",
            cpu_threads=cpu_threads
        )
        self.sample_rate = sample_rate
        self.device = device
        self.language = language
        self.beam_size = beam_size
        self.audio_buffer = []
        self.stream = None

    def _callback(self, indata, frames, time, status):
        """Collects audio while recording is active."""
        self.audio_buffer.append(indata.copy())

    def start_recording(self):
        """Start capturing audio."""
        self.audio_buffer.clear()
        self.stream = sd.InputStream(
            samplerate=self.sample_rate, channels=1, dtype=np.float32, device=self.device, callback=self._callback
        )
        self.stream.start()

    def stop_recording(self):
        """Stop recording and return the transcribed text."""
        if self.stream:
            self.stream.stop()
            self.stream.close()
            self.stream = None

        if not self.audio_buffer:
            return ""

        # Convert recorded chunks into a single array
        audio = np.concatenate(self.audio_buffer, axis=0).flatten()
        
        # Transcribe audio
        segments, _ = self.model.transcribe(
            audio,
            beam_size=self.beam_size,
            language=self.language,
            vad_filter=True
        )

        # Return transcribed text
        return "".join(segment.text for segment in segments)

# # Example usage
# result = speech2text()
# print("Final result:", result)




# TODO: user a offline version When you got a Nvidia GPU 

def text_to_speech_gtts(text, lang='en'): # Added slow parameter
    tts = gTTS(text=text, lang=lang, slow=False) # slow=True for slower speed
    tts.save("output.mp3")
    os.system("mpg123 output.mp3") #for linux
    #os.system("start output.mp3")  # For Windows
    #from playsound import playsound #for windows
    #playsound("output.mp3")

def IOT_control(name):
    text_to_speech_gtts("sorry, IOT Controal feature is not avvalable")

def open_application(app_name):
    """Prompt the user for an application name and attempt to open it."""
    # Get the list of installed applications from /usr/bin
    bin_path = "/usr/bin"
    if not os.path.exists(bin_path):
        print("Error: /usr/bin not found.")
        return

    installed_apps = [app.lower() for app in os.listdir(bin_path)]

    # Get user input for the application name
    app_name = app_name.strip().lower()

    # Check for exact match first
    if app_name in installed_apps:
        matched_app = app_name
    else:
        # Use difflib for closest matches
        closest_matches = difflib.get_close_matches(app_name, installed_apps, n=3, cutoff=0.6)
        matched_app = closest_matches[0] if closest_matches else None

    # Handle the case where no match is found
    if not matched_app:
        text_to_speech_gtts(f"No match found for '{app_name}'. Please check the name and try again.")
        return

    text_to_speech_gtts(f"Opening: {matched_app}")

    # Try to open the application
    try:
        subprocess.run([matched_app], check=True)
    except FileNotFoundError:
        text_to_speech_gtts(f"Application '{matched_app}' not found or could not be opened.")
    except Exception as e:
        text_to_speech_gtts(f"An error occurred: {e}")


if __name__ == "__main__":
    text_to_speech_gtts()
    IOT_control()
    open_application()
