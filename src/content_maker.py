import os

from openai import OpenAI
from src.steps.file_converter import FileConverter
from src.steps.audio_transcriber import AudioTranscriber
from src.steps.transcription_analyzer import TranscriptionAnalyzer
from src.steps.script_generator import ScriptGenerator
from src.steps.image_describer import ImageDescriber
from src.steps.image_generator import ImageGenerator

class ContentMaker:
    def __init__(self, input_path, output_folder, openai_api_key=None):
        self.original_file_name = input_path.rsplit('.', 1)[0] + '.wav'
        self.input_path = input_path
        self.output_folder = output_folder
        self.openai = OpenAI(api_key = os.environ.get("OPEN_AI_API_KEY", openai_api_key))
        
        self.file_converter = FileConverter(output_folder, self.openai)
        self.audio_transcriber = AudioTranscriber(output_folder, self.openai)
        self.transcription_analyzer = TranscriptionAnalyzer(output_folder, self.openai)
        self.script_generator = ScriptGenerator(output_folder, self.openai)
        self.image_describer = ImageDescriber(output_folder, self.openai)
        self.image_generator = ImageGenerator(output_folder, self.openai)
      
    def execute(self):
        # Step 1. Ensure the input audio format is suitable for whisper AI
        self.convert_file()
        
        # Step 2. Transcribe the input audio and save text
        self.transcribe_wav(self.file_converter_result)
        
        # Step 3. Analyze the text and create a script
        self.analyze_transcription(self.audio_transcriber_result)
        
        # Step 4. Create a script from the analysis for episodes
        self.generate_script(self.transcription_analyzer_result)
        
        # Step 5. Generate description for episode images
        self.describe_images(self.script_generator_result)
        
        # Step 6. Generate images
        self.image_urls = self.generate_images()
        
    def convert_file(self):
        self.file_converter_result = self.file_converter.execute(self.input_path)
        
    def transcribe_wav(self, wav_path):
        self.audio_transcriber_result = self.audio_transcriber.execute(wav_path)
        
    def analyze_transcription(self, transcription):
        self.transcription_analyzer_result = self.transcription_analyzer.execute(transcription)

    def generate_script(self, analysis):
        self.script_generator_result = self.script_generator.execute(analysis)
        
    def describe_images(self, script: str):
        self.image_describer_result = self.image_describer.execute(script)

    def generate_images(self, image_descriptions: str):
        self.image_generator_result = self.image_generator.execute(image_descriptions)
