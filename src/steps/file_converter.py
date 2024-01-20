import os
from pydub import AudioSegment

from src.steps.base_step import BaseStep

class FileConverter(BaseStep):
    def __init__(self, output_folder,  openai):
        super().__init__('FileConverter', output_folder, openai)
        
    def execute(self, input_path: str):
        self.log('1. Starting file conversion...')
        try:
            # Load the input file
            audio = AudioSegment.from_file(input_path)

            # Set file output format
            output_path = self.get_path('input.wav')

            # Export the file as a WAV
            audio.export(output_path, format='wav', parameters=["-ac", "1", "-ar", "16000"])

            self.log(f'1. File conversion complete. Result is saved to: {output_path}')
            return output_path

        except Exception as e:
            self.log(f"An error occurred during file conversion: {str(e)}")
            return None
