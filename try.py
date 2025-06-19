import os
import wave
import json
import pandas as pd
from vosk import Model, KaldiRecognizer

def transcribe_audio(audio_file_path):
    model_path = "vosk-model-small-en-us-0.15"

    wf = wave.open(audio_file_path, "rb")
    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getframerate() != 16000:
        raise ValueError(f"{audio_file_path} must be mono, 16-bit, 16kHz")

    model = Model(model_path)
    rec = KaldiRecognizer(model, wf.getframerate())

    results = []
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            results.append(json.loads(rec.Result()))
    results.append(json.loads(rec.FinalResult()))

    transcript = " ".join(r.get("text", "") for r in results)
    return transcript

def process_all_audio_files(csv_path="trailerData.csv", audio_folder="audios"):
    df = pd.read_csv(csv_path)

    if 'transcript' not in df.columns:
        df['transcript'] = ""

    model_path = "vosk-model-small-en-us-0.15"
    model = Model(model_path)

    for idx, row in df.iterrows():
        audio_filename = row['audio_file']
        audio_path = os.path.join(audio_folder, audio_filename)

        if not os.path.isfile(audio_path):
            print(f"[SKIPPED] File not found: {audio_filename}")
            continue

        # print(f"[PROCESSING] {audio_filename}")
        try:
            wf = wave.open(audio_path, "rb")
            if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getframerate() != 16000:
                print(f"[SKIPPED] Invalid format: {audio_filename}")
                continue

            rec = KaldiRecognizer(model, wf.getframerate())
            results = []

            while True:
                data = wf.readframes(4000)
                if len(data) == 0:
                    break
                if rec.AcceptWaveform(data):
                    results.append(json.loads(rec.Result()))
            results.append(json.loads(rec.FinalResult()))

            transcript = " ".join(r.get("text", "") for r in results)
            df.at[idx, 'transcript'] = transcript
            print(f"[DONE] Transcript added for: {audio_filename}")

        except Exception as e:
            print(f"[ERROR] {audio_filename}: {e}")

    df.to_csv(csv_path, index=False)
    print("[FINISHED] CSV updated.")

# Run the full processing
process_all_audio_files()
