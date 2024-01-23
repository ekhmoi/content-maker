import datetime
import json
from openai import OpenAI
from src.steps.audio_transcriber import AudioTranscriber
from src.steps.text_analyzer import TextAnalyzer
from src.steps.script_generator import ScriptGenerator
from src.steps.image_describer import ImageDescriber
from src.steps.image_generator import ImageGenerator
from src.steps.input_converter import InputConverter
import os

class ContentStepExecutor:
    def __init__(self, startStep, input_path, output_folder, openai_api_key, message_queue):
        print(f'[ContentStepExecutor]: 0 - Initializing ContentMaker with step: {startStep}, output_folder: {output_folder}, openai_api_key: {openai_api_key}')
        self.startStep = startStep
        self.input_path = input_path
        self.output_folder = output_folder
        self.openai = OpenAI(api_key =  openai_api_key)
        self.results = {}
        self.message_queue = message_queue
        
        self.input_converter = InputConverter(output_folder, self.openai, self.message_queue)
        self.audio_transcriber = AudioTranscriber(output_folder, self.openai, self.message_queue)
        self.text_analyzer = TextAnalyzer(output_folder, self.openai, self.message_queue)
        self.script_generator = ScriptGenerator(output_folder, self.openai, self.message_queue)
        self.image_describer = ImageDescriber(output_folder, self.openai, self.message_queue)
        self.image_generator = ImageGenerator(output_folder, self.openai, self.message_queue)

        self.steps = [
            {'step': self.input_converter, 'step_name': self.input_converter.step_name},
            {'step': self.audio_transcriber, 'step_name': self.audio_transcriber.step_name},
            {'step': self.text_analyzer, 'step_name': self.text_analyzer.step_name},
            {'step': self.script_generator, 'step_name': self.script_generator.step_name},
            {'step': self.image_describer, 'step_name': self.image_describer.step_name},
            {'step': self.image_generator, 'step_name': self.image_generator.step_name}
        ]
        
        self.init_content_repository()
        
    def init_content_repository(self):
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)
            self.metadata = {
                'created_at': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'folder_name': self.output_folder, 
                'initial_input': self.input_path 
            }
            with open(self.output_folder + '/manifest.json', 'w', encoding='utf-8') as output_file:
                output_file.write(json.dumps(self.metadata))
      
    def execute(self):
        # The initial input for the first step
        step_input = self.input_path if self.startStep == 0 else self.read_file(self.input_path)

        # Loop over the steps starting from self.step
        for current_step in self.steps[self.startStep:]:
            step_function = current_step['step'].execute
            step_name = current_step['step_name']
            step_result = step_function(step_input)

            # Pass the result as input to the next step
            step_input = step_result

            # Store the result in the results dictionary
            self.results[step_name] = step_result

    def execute_step(self):
        step_to_execute = self.steps[self.startStep]
        step_input = self.input_path if self.startStep < 2 else self.read_file(self.input_path)
        return step_to_execute['step'].execute(step_input)

    def read_file(self, file_path: str):
        with open(file_path, 'r') as file:
            return file.read()