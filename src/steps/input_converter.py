from pytube import YouTube
from pydub import AudioSegment

from moviepy.editor import *
import os


from src.steps.base_step import BaseStep

class InputConverter(BaseStep):
    def __init__(self, output_folder, openai):
        super().__init__('InputConverter', output_folder, openai)

    def execute(self, url: str):
        wav_file = None
        if url.startswith('https://youtube.com') or url.startswith('https://www.youtube.com'):
            self.log("Starting download from youtube...")
            video_file = self.download_video(url)
            self.log("Download completed.")
            self.log("Converting to wav...")
            wav_file = self.convert_to_wav(video_file)
            self.log("Conversion completed")
            final_path = os.path.join(self.output_folder, 'input.wav')
            os.rename(wav_file, final_path)
            return final_path
        else:
            return self.convert_local_file(url)
            

    def download_video(self, url):
        yt = YouTube(url)
        video = yt.streams.filter(only_audio=True).first()
        return video.download(output_path=self.output_folder)

    def convert_to_wav(self, filename):
        clip = AudioFileClip(filename)
        wav_filename = filename.replace('.mp4', '.wav')
        clip.write_audiofile(wav_filename, codec='pcm_s16le')
        os.remove(filename)  # Remove the original download
        return wav_filename


    def convert_local_file(self, input_path: str):
        self.log('1 - Starting file conversion...')
        try:
            # Load the input file
            audio = AudioSegment.from_file(input_path)

            # Set file output format
            output_path = self.get_path('input.wav')

            # Export the file as a WAV
            audio.export(output_path, format='wav', parameters=["-ac", "1", "-ar", "16000"])

            self.log(f'1 - File conversion complete - Result is saved to: {output_path}')
            return output_path

        except Exception as e:
            self.log(f"An error occurred during file conversion: {str(e)}")
            return None
