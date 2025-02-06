import time
import json
from pynput import keyboard as pk
import functions as func
import Ollama_with_prompt as op

# Create your recognizer once
recognizer = func.SpeechRecognizer()

# Global flag to indicate if we're recording
recording = False
# Set to track currently pressed keys
pressed_keys = set()

def process_transcription(voice):
    """Process and display the transcription."""
    print("Transcribed:", voice)
    check = op.search_needed(voice, model="deepseek-r1:1.5b")
    print("Check:", check)
    if 'INTERNET_REQUIRED' in check:
        print("Wait, searching through the web...\n")
        text = op.scrap_text(voice)
        i_dont_know = f'Gathered information\n Context: {text}, user input: {voice}'
        print('I don’t know:', i_dont_know)
        ollama_prompt = op.Ollama(i_dont_know)
        print("Ollama:", ollama_prompt)
        if ollama_prompt.startswith("@Open"):
            func.open_application(ollama_prompt.replace("@Open", "").strip())
        print("\n")
    else:
        ollama_prompt = op.Ollama(voice)
        print("Ollama:", ollama_prompt)
        if ollama_prompt.startswith("@Open"):
            func.open_application(ollama_prompt.replace("@Open", "").strip())

def on_press(key):
    global recording
    # Add the key to our set
    pressed_keys.add(key)

    # Check if any variant of CTRL and ALT are currently pressed.
    ctrl_keys = {pk.Key.ctrl, pk.Key.ctrl_l, pk.Key.ctrl_r}
    alt_keys  = {pk.Key.alt, pk.Key.alt_l, pk.Key.alt_r}

    if not recording and pressed_keys.intersection(ctrl_keys) and pressed_keys.intersection(alt_keys):
        # Both CTRL and ALT are pressed; start recording.
        recording = True
        print("Recording started... (Release CTRL or ALT to stop)")
        recognizer.start_recording()

def on_release(key):
    global recording
    try:
        pressed_keys.remove(key)
    except KeyError:
        pass

    ctrl_keys = {pk.Key.ctrl, pk.Key.ctrl_l, pk.Key.ctrl_r}
    alt_keys  = {pk.Key.alt, pk.Key.alt_l, pk.Key.alt_r}

    # If we are recording but one (or both) of CTRL or ALT are no longer pressed,
    # stop recording.
    if recording and (not pressed_keys.intersection(ctrl_keys) or not pressed_keys.intersection(alt_keys)):
        recording = False
        voice = recognizer.stop_recording()
        if voice.strip():
            process_transcription(voice)
        else:
            print("No audio detected; please try again.")

    # Optionally, allow a way to exit the listener (e.g. with ESC)
   

print("Ready. Hold CTRL+ALT to record; release them to stop.")
with pk.Listener(on_press=on_press, on_release=on_release) as listener:
    try:
        listener.join()
    except KeyboardInterrupt:
        # On Ctrl+C exit, perform any necessary cleanup
        try:
            with open("/home/tahmid/programming file/virtual assistant/data.json", "r") as f:
                data = json.load(f)
            data["messages_needed"] = [msg for msg in data["messages_needed"] if msg["role"] not in ['user', 'assistant']]
            data["messages_main_AI"] = [msg for msg in data["messages_main_AI"] if msg["role"] not in ['user', 'assistant']]
            with open("/home/tahmid/programming file/virtual assistant/data.json", "w") as f:
                json.dump(data, f, indent=4)
            print("User and assistant data have been removed.")
        except Exception as e:
            print("Error during cleanup:", e)
