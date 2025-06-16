import os
import pandas as pd
import subprocess

directoryy = "trailers"
os.makedirs(directoryy, exist_ok=True)
df = pd.read_csv("trailer_address.csv")
trailer_amount =80
df = df.head(trailer_amount)
for idx, row in df.iterrows():
    video_id = row['youtubeId']
    title = row['title'].replace(" ", "_").replace("/", "_")
    output_path = os.path.join(directoryy, f"{title}_{video_id}.mp4")
    if not os.path.exists(output_path):
        print(f"Downloading {title}...")
        command = f'yt-dlp -f mp4 -o "{output_path}" https://www.youtube.com/watch?v={video_id}'
        subprocess.run(command, shell=True)

print(f"First {trailer_amount} trailers downloaded")