import os
from google.cloud import speech_v1p1beta1 as speech  # Use extended version
import time

# Path to your Google Cloud credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "afiniti-ml.json"

client = speech.SpeechClient()

file_name = "audios/'Til_There_Was_You_(1997)_8VFQ9qzRbgI.wav"

with open(file_name, "rb") as f:
    byte_data = f.read()

audio = speech.RecognitionAudio(content=byte_data)

config = speech.RecognitionConfig(
    encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
    sample_rate_hertz=16000,  # adjust if needed
    language_code="en-UK",
    enable_automatic_punctuation=True,
)

# Use long-running recognize for large files
operation = client.long_running_recognize(config=config, audio=audio)
print("Processing audio file...")

response = operation.result(timeout=300)

# Print transcript
for result in response.results:
    print("Transcript:", result.alternatives[0].transcript)
    print("Confidence:", result.alternatives[0].confidence)
