import os

from src.steps.base_step import BaseStep

class TranscriptionAnalyzer(BaseStep):
    def __init__(self, openai):
        super().__init__(openai, 'TranscriptionAnalyzer')
    
    def execute(self, transcription: str, output_folder: str, original_file_name: str):
        self.log('Starting analysis...')
        try:
            response = self.openai.chat.completions.create(
                model="gpt-3.5-turbo",  # or another appropriate model
                messages=[
                    {"role": "system", "content": "Analyze this text and provide key themes and insights"},
                    {"role": "user", "content": transcription}
                ]
            )
            analysis_file_path = os.path.join(output_folder, f"{original_file_name}-analysis.txt")
            with open(analysis_file_path, 'w', encoding='utf-8') as file:
                file.write(response.choices[0].message.content)
            self.log('Analysis complete. Result is saved to' + analysis_file_path)
            return response.choices[0].message.content
        except Exception as e:
            print(f"An error occurred: {e}")
            return None