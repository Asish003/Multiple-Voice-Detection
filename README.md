# Multiple-Voice-Detection

A Python-based voice-to-text converter utilizing models like Vosk for speech recognition. The primary goal of this project is to generate a transcript (.txt) of an entire conversation while identifying different speakers.

### Current Features:
- Converts speech to text using the Vosk model.
- Detects and labels speakers (currently limited to one-person detection).
- Saves the transcribed text in a designated folder.

### Future Improvements:
- Enhanced speaker diarization (multi-speaker recognition).
- Improved neural network for voice detection.

## Setup Instructions

### 1. Create a Virtual Environment
Before running the program, create a Python virtual environment:
```sh
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate    # On Windows
```

### 2. Install Dependencies
Run the following command to install the required packages:
```sh
pip install -r requirements.txt
```

### 3. Create Necessary Directories
Ensure the following directories exist before running the program:
```sh
mkdir Recorded_Audio
mkdir Recorded_Text
```
Alternatively, manually create:
- `Recorded_Audio`: Directory to store recorded audio files.
- `Recorded_Text`: Directory to store transcribed text files.

### 4. Download and Set Up the Vosk Model
Download a Vosk speech recognition model from [Vosk Models](https://alphacephei.com/vosk/models) and specify the model path in your script:
```python
MODEL_PATH = "vosk-model-small-en-us-0.15"
```
Note: Larger models provide better accuracy but increase processing time.

### 5. Run the Program
Execute the following command in your terminal:
```sh
python main_vosk.py
```
Once the recording starts, you will see:
```
Recording... Press CTRL + C to stop
```

### Notes:
- The heavier the model, the longer the transcription process.
- Currently, transcription is only available in English.
- Speaker recognition using neural networks is still under development.

---

Feel free to contribute to the project by improving speaker detection or adding support for additional languages!

