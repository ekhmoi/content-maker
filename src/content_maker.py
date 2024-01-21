from openai import OpenAI
from src.steps.file_converter import FileConverter
from src.steps.audio_transcriber import AudioTranscriber
from src.steps.text_analyzer import TextAnalyzer
from src.steps.script_generator import ScriptGenerator
from src.steps.image_describer import ImageDescriber
from src.steps.image_generator import ImageGenerator

class ContentMaker:
    def __init__(self, step, input_path, output_folder, openai_api_key):
        print(f'[ContentMaker]: 0 - Initializing ContentMaker with step: {step}, output_folder: {output_folder}, openai_api_key: {openai_api_key}')
        self.step = step
        self.input_path = input_path
        self.output_folder = output_folder
        self.openai = OpenAI(api_key =  openai_api_key)
        self.results = {}

        self.file_converter = FileConverter(output_folder, self.openai)
        self.audio_transcriber = AudioTranscriber(output_folder, self.openai)
        self.text_analyzer = TextAnalyzer(output_folder, self.openai)
        self.script_generator = ScriptGenerator(output_folder, self.openai)
        self.image_describer = ImageDescriber(output_folder, self.openai)
        self.image_generator = ImageGenerator(output_folder, self.openai)

        self.steps = [
            {'step': self.file_converter, 'step_name': self.file_converter.step_name},
            {'step': self.audio_transcriber, 'step_name': self.audio_transcriber.step_name},
            {'step': self.text_analyzer, 'step_name': self.text_analyzer.step_name},
            {'step': self.script_generator, 'step_name': self.script_generator.step_name},
            {'step': self.image_describer, 'step_name': self.image_describer.step_name},
            {'step': self.image_generator, 'step_name': self.image_generator.step_name}
        ]
      
    def execute(self):
        # The initial input for the first step
        step_input = self.input_path if self.step == 0 else self.read_file(self.input_path)

        # Loop over the steps starting from self.step
        for current_step in self.steps[self.step:]:
            step_function = current_step['step'].execute
            step_name = current_step['step_name']
            step_result = step_function(step_input)

            # Pass the result as input to the next step
            step_input = step_result

            # Store the result in the results dictionary
            self.results[step_name] = step_result



    def read_file(self, file_path: str):
        with open(file_path, 'r') as file:
            return file.read()