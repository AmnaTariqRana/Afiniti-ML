from vosk import Model, KaldiRecognizer
import wave
import json
import os

model_path = "vosk-model-small-en-us-0.15"
wf = wave.open("audios/Toy_Story_(1995)_K26_sDKnvMU.wav", "rb")

if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getframerate() != 16000:
    raise ValueError("Audio file must be mono, 16-bit, 16kHz")

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

# Join all text parts
transcript = " ".join(r.get("text", "") for r in results)
print("Transcript:", transcript)
