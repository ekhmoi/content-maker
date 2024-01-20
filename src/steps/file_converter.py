import subprocess
import os

from src.steps.base_step import BaseStep

class FileConverter(BaseStep):
    def __init__(self, openai):
        super().__init__(openai, 'FileConverter')
        
    def execute(self, input_path, output_folder):
        self.log('Starting file conversion...')
        original_file_name = input_path.rsplit('.', 1)[0] + '.wav'
        output_path = os.path.join(output_folder, os.path.splitext(original_file_name)[0] + '.wav')
        command = [
            'ffmpeg', 
            '-err_detect', 'ignore_err',
            '-analyzeduration', '2147483647',  # Max possible value for analyzeduration
            '-probesize', '2147483647',       # Max possible value for probesize
            '-i', input_path, 
            '-acodec', 'pcm_s16le',
            '-ar', '16000',
            '-ac', '1',
            output_path
        ]
        subprocess.run(command)
        self.log('File conversion complete. Result is saved to' + output_path)
        return output_path