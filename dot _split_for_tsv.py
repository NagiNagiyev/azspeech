import os
import pandas as pd 
from pydub import AudioSegment
from pydub.playback import play

# function to split sentences according "."
def merge_sentences(df):
    merged_rows = []
    current_start = df['start'].iloc[0]
    current_text = df['text'].iloc[0]

    for i in range(1, len(df)):
        if not current_text.endswith("."):
            current_text += " " + df['text'].iloc[i]
        else:
            merged_rows.append({'start': current_start, 'end': df['end'].iloc[i - 1], 'text': current_text})
            current_start = df['start'].iloc[i]
            current_text = df['text'].iloc[i]

    merged_rows.append({'start': current_start, 'end': df['end'].iloc[-1], 'text': current_text})
    return pd.DataFrame(merged_rows)

if __name__ == "__main__":

    # code store texts(as txt files) and their audios(as mp3 files) in local storages with number file names
    # this code is to get biggest number file name in the specified folder to prevent overwriting files 
    # change directory path to yours where you want to store files
    folder_path = "C:\\Users\\user\\Downloads\\voice_folder"
    files = os.listdir(folder_path)
    mp3_files = [file for file in files if file.endswith(".mp3")]
    max_number = max(int(file.split(".")[0]) for file in mp3_files)
    file_count = max_number + 1

    # give the path for tsv file
    table = pd.read_csv("C:\\Users\\user\\Downloads\\audio1.tsv", sep='\t')
    table.columns = ["start", "end", "text"]
    table_merged = merge_sentences(table)

    # give the path for mp3 file
    original_audio = AudioSegment.from_file("C:\\Users\\user\\Downloads\\test.mp3", format="mp3")

    # this code will save all audios with their text separately
    for start, end, text in zip(table_merged['start'].values, table_merged['end'].values, table_merged['text'].values):
        start_time = start - 250
        end_time = end + 250

        extracted_segment = original_audio[start_time:end_time]
        extracted_segment.export(f"C:\\Users\\user\\Downloads\\voice_folder\\{file_count}.mp3", format="mp3")
        with open(f"C:\\Users\\user\\Downloads\\voice_folder\\{file_count}.txt", 'w', encoding='utf-8') as file:
            file.write(text)
        file_count = file_count + 1