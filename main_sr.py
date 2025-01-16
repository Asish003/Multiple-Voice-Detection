import os
import pyaudio
import speech_recognition as sr
import wave
from io import BytesIO

from datetime import datetime
current_time = datetime.now().strftime("%Y%m%d_%H%M%S")


FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024

folder_path_audio = "D:\current_project\Multiple-Voice-Detection\Recorded_Audio"
folder_path_text = "D:\current_project\Multiple-Voice-Detection\Recorded_Text"

os.makedirs(folder_path_audio, exist_ok=True)
os.makedirs(folder_path_text, exist_ok=True)

OUTPUT_FILEANME = os.path.join(folder_path_audio, f'output_{current_time}.wav')
TEXT_FILENAME = os.path.join(folder_path_text, f'output_{current_time}.txt')

p = pyaudio.PyAudio()
recognizer = sr.Recognizer()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print('Recording... Press CTRL + C to stop')

frames = []

try:
    with open(TEXT_FILENAME,'w') as text_file:
        while True:
            data = stream.read(CHUNK)
            frames.append(data)

            audio_stream = BytesIO(data)
            audio_chunk = sr.AudioFile(audio_stream)

            try:
                with audio_chunk as source:
                    audio_data = recognizer.record(source)
                text = recognizer.recognize_google(audio_data)
                print(f"Recognized--> {text}")
                text_file.write(f"{text}\n")
            except sr.UnknownValueError:
                pass
            except sr.RequestError as e:
                print(f"Error with request: {e}")

except KeyboardInterrupt:
    print("Recording Stopped")
    stream.stop_stream()
    stream.close()
    p.terminate()


    with wave.open(OUTPUT_FILEANME,'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))

    print(f"Audio---->{OUTPUT_FILEANME}")
    print(f"Text----->{TEXT_FILENAME}")