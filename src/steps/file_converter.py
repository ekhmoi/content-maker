import os
from pydub import AudioSegment

from src.steps.base_step import BaseStep

class FileConverter(BaseStep):
    def __init__(self, openai):
        super().__init__(openai, 'FileConverter')
        
    def execute(self, input_path, output_folder):
        self.log('Starting file conversion...')
        try:
            # Load the input file
            audio = AudioSegment.from_file(input_path)

            # Set file output format
            original_file_name = os.path.splitext(os.path.basename(input_path))[0]
            output_path = os.path.join(output_folder, original_file_name + '.wav')

            # Export the file as a WAV
            audio.export(output_path, format='wav', parameters=["-ac", "1", "-ar", "16000"])

            self.log('File conversion complete. Result is saved to ' + output_path)
            return output_path

        except Exception as e:
            self.log(f"An error occurred during file conversion: {str(e)}")
            return None
