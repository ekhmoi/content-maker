import os

from src.steps.base_step import BaseStep

class ScriptGenerator(BaseStep):
    openaiPrompt = """
        Create a script for an animated episode based on this content
    """
    def __init__(self, openai):
        super().__init__(openai, 'ScriptGenerator')
    
    def execute(self, analysis: str, output_folder: str, original_file_name: str):
        self.log('Starting script generation...')
        try:
            response = self.openai.chat.completions.create(
                model="gpt-3.5-turbo",  # or another appropriate model
                messages=[
                    {"role": "system", "content": self.openaiPrompt},
                    {"role": "user", "content": analysis}
                ]
            )
            result = response.choices[0].message.content
            self.save_result(os.path.join(output_folder, f"{original_file_name}-script.txt"), result)
            self.log('Script generation complete. Result is saved to' + os.path.join(output_folder, f"{original_file_name}-script.txt"))
            return result
        except Exception as e:
            self.log(f"An error occurred: {e}")
            return None
        