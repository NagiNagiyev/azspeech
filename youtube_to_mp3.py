from pytube import YouTube
from moviepy.video.io.VideoFileClip import VideoFileClip
import os

# download video
def download_video(youtube_url, output_path='.'):
    try:
        yt = YouTube(youtube_url)
        video_stream = yt.streams.get_highest_resolution()
        video_stream.download(output_path)

        video_filename = video_stream.title + ".mp4"
        video_path = os.path.join(output_path, video_filename)
        return video_path

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# extract mp3 from video
def extract_audio(video_path, audio_output_path):
    video_clip = VideoFileClip(video_path)
    audio_clip = video_clip.audio
    audio_clip.write_audiofile(audio_output_path)
    video_clip.close()
    audio_clip.close()

# delete mp4 because there is no need for it 
def delete_mp4_files(folder_path):
    files = os.listdir(folder_path)
    for file in files:
        if file.lower().endswith('.mp4'):
            file_path = os.path.join(folder_path, file)
            os.remove(file_path)

# function is used to apply "extract_audio" function to all mp4 files in the folder 
def extract_audio_from_folder(folder_path, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    files = os.listdir(folder_path)

    for file in files:
        if file.lower().endswith('.mp4'):
            video_path = os.path.join(folder_path, file)
            audio_output_path = os.path.join(output_folder, f'{os.path.splitext(file)[0]}.mp3')
            extract_audio(video_path, audio_output_path)

if __name__ == "__main__":

    urls_list = ["YOUTUBE_LINK"]
    for url in urls_list:
        video_url = url
        #path to specify where to download mp3 file
        folder = r'C:\Users\user\Downloads\voice_folder'
        path = download_video(video_url, output_path=folder)
        extract_audio_from_folder(folder, folder)
        delete_mp4_files(folder)
        print("MP3 file downloaded!")