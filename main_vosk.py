import os
import wave
from vosk import Model, KaldiRecognizer
import json
from datetime import datetime
import pyaudio

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024

current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
folder_path_audio = "D:\\current_project\\Multiple-Voice-Detection\\Recorded_Audio"
folder_path_text = "D:\\current_project\\Multiple-Voice-Detection\\Recorded_Text"

os.makedirs(folder_path_audio, exist_ok=True)
os.makedirs(folder_path_text, exist_ok=True)

OUTPUT_FILENAME = os.path.join(folder_path_audio, f'output_{current_time}.wav')
TEXT_FILENAME = os.path.join(folder_path_text, f'output_{current_time}.txt')

MODEL_PATH = "vosk-model-small-en-us-0.15" 
if not os.path.exists(MODEL_PATH):
    print(f"Model not found at {MODEL_PATH}. <<<<<<Please download a model>>>>>>")
    exit(1)

model = Model(MODEL_PATH)
recognizer = KaldiRecognizer(model, RATE)

p = pyaudio.PyAudio()
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print("Recording... Press CTRL + C to stop")
frames = []

try:
    while True:
        data = stream.read(CHUNK)
        frames.append(data)

except KeyboardInterrupt:
    print("Recording Stopped")
    stream.stop_stream()
    stream.close()
    p.terminate()

    with wave.open(OUTPUT_FILENAME, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))

    print(f"Audio saved to: {OUTPUT_FILENAME}")

    with wave.open(OUTPUT_FILENAME, 'rb') as wf:
        recognizer = KaldiRecognizer(model, wf.getframerate())
        text_output = []

        while True:
            data = wf.readframes(CHUNK)
            if len(data) == 0:
                break

            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                text = result.get("text", "").strip()
                if text:
                    text_output.append(text) 

        final_result = json.loads(recognizer.FinalResult())
        final_text = final_result.get("text", "").strip()
        if final_text:
            text_output.append(final_text)

        print("Full Transcription Results:", text_output)

        with open(TEXT_FILENAME, 'w') as text_file:
            text_file.write("\n".join(text_output))

    print(f"Transcriptions saved to: {TEXT_FILENAME}")
