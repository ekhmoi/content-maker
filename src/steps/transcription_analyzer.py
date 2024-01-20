import os

from src.steps.base_step import BaseStep

class TranscriptionAnalyzer(BaseStep):
    def __init__(self, output_folder,  openai):
        super().__init__('TranscriptionAnalyzer', output_folder, openai)
    
    def execute(self, transcription: str):
        self.log('3. Starting analysis...')
        try:
            response = self.openai.chat.completions.create(
                model="gpt-3.5-turbo",  # or another appropriate model
                messages=[
                    {"role": "system", "content": "Analyze this text and provide key themes and insights"},
                    {"role": "user", "content": transcription}
                ]
            )
            result = response.choices[0].message.content
            analysis_file_path = os.path.join(self.output_folder, "transcription_analyzer_result.txt")

            self.save_result(analysis_file_path, result)
            self.log(f'3. Analysis complete. Result is saved to: {analysis_file_path}')

            return result
        except Exception as e:
            print(f"An error occurred: {e}")
            return None