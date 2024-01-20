import os

from src.steps.base_step import BaseStep

class ScriptGenerator(BaseStep):
    def __init__(self, output_folder, openai):
        super().__init__('ScriptGenerator', output_folder, openai)
    
    def execute(self, analysis: str):
        self.log('4. Starting script generation...')
        try:
            response = self.openai.chat.completions.create(
                model="gpt-3.5-turbo",  # or another appropriate model
                messages=[
                    {"role": "system", "content": "Create a script for an animated episode based on this content"},
                    {"role": "user", "content": analysis}
                ]
            )
            result = response.choices[0].message.content
            result_path = self.get_path("script_generator_result")
            self.save_result(result_path, result)
            self.log(f'4. Script generation complete. Result is saved to: {result_path}')
            
            return result
        except Exception as e:
            self.log(f"An error occurred: {e}")
            return None
        