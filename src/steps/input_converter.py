from pytube import YouTube
from pydub import AudioSegment

from moviepy.editor import *
import os


from src.steps.base_step import BaseStep

class InputConverter(BaseStep):
    def __init__(self, *args):
        super().__init__('input_converter', *args)

    def execute(self, url: str):
        wav_file = None
        if url.startswith('https://youtube.com') or url.startswith('https://www.youtube.com'):
            video_file = self.download_video(url)
            wav_file = self.convert_to_wav(video_file)
            final_path = self.get_path('input.wav')
            os.rename(wav_file, final_path)

            return self.convert_local_file(final_path)
        else:
            return self.convert_local_file(url)
            

    def download_video(self, url):
        self.send_message('download_video_start', {'step': 1, 'title': self.output_folder})

        yt = YouTube(url)
        self.update_metadata('video_title', yt.title)
        video = yt.streams.filter(only_audio=True).first()
        video_url = video.download(output_path=self.output_folder)

        self.send_message('download_video_end', {'step': 1, 'title': self.output_folder})

        return video_url

    def convert_to_wav(self, filename):
        self.send_message('convert_to_wav_start', {'step': 1, 'title': self.output_folder})

        clip = AudioFileClip(filename)
        wav_filename = filename.replace('.mp4', '.wav')
        clip.write_audiofile(wav_filename, codec='pcm_s16le')
        os.remove(filename)  # Remove the original download

        self.send_message('convert_to_wav_end', {'step': 1, 'title': self.output_folder})
        return wav_filename


    def convert_local_file(self, input_path: str):
        self.send_message('convert_local_file_start', {'step': 1, 'title': self.output_folder})
        try:
            # Load the input file
            audio = AudioSegment.from_file(input_path)

            # Set file output format
            output_path = self.get_path('input.wav')

            # Export the file as a WAV
            audio.export(output_path, format='wav', parameters=["-ac", "1", "-ar", "8000"])

            self.send_message('convert_local_file_end', {'step': 1, 'title': self.output_folder})
            return output_path

        except Exception as e:
            self.log(f"An error occurred during file conversion: {str(e)}")
            self.send_message('convert_local_file_failed', {'step': 1, 'title': self.output_folder})
            return None
