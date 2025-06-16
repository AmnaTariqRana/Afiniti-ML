import os
import pandas as pd
import subprocess

directoryy = "trailers"
os.makedirs(directoryy, exist_ok=True)
data_csv = "trailerData.csv"
if os.path.exists(data_csv):
    existing_df = pd.read_csv(data_csv)
else:
    existing_df = pd.DataFrame(columns=["file_name", "movie_name", "genre", "transcript"])



df = pd.read_csv("trailer_address.csv")
trailer_amount = 80
df = df.head(trailer_amount)
rows_to_append = []
for idx, row in df.iterrows():
    video_id = row['youtubeId']
    title = row['title'].replace(" ", "_").replace("/", "_")
    file_name = f"{title}_{video_id}.mp4"
    output_path = os.path.join(directoryy, file_name)
# no duplicate entries
    if not ((existing_df['file_name'] == file_name).any()):
        if not os.path.exists(output_path):
            print(f"Downloading {title}...")
            command = f'yt-dlp -f mp4 -o "{output_path}" https://www.youtube.com/watch?v={video_id}'
            subprocess.run(command, shell=True)
            if os.path.exists(output_path):#    if download succeeded
                rows_to_append.append([file_name, row['title'], "", ""])
        else:
            print(f"{title} already exists.")
            rows_to_append.append([file_name, row['title'], "", ""])

if rows_to_append:# new rows and saving
    new_df = pd.DataFrame(rows_to_append, columns=["file_name", "movie_name", "genre", "transcript"])
    updated_df = pd.concat([existing_df, new_df], ignore_index=True)
    updated_df.to_csv(data_csv, index=False)
    print(f"Updated {data_csv} with {len(rows_to_append)} entries.")
else:
    print("No new entries added to trailerData.csv")

print(f"First {trailer_amount} trailers processed.")
