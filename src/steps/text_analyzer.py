from src.steps.base_step import BaseStep
import ollama
import json

# response = 
# print(response['message']['content'])


class TextAnalyzer(BaseStep):
    openai_prompt = '''
        Analyze this text and provide key themes and insights with detailed descriptions.
        Return the items in a JSON array.
        Use provided function 'analyze_text' for response.
    '''

    def __init__(self, *args):
        super().__init__('text_analyzer', *args)
    
    def execute(self, text: str):
        self.log('3 - Starting analysis of text: ' + text)
        try:
            self.send_message('executing_step', {'step': 3, 'title': self.output_folder})
            template = {'key_points': ["keypoint1", "keypoint2", "keypoint3"]}
            response = ollama.chat(model='llama2', messages=[
                {'role': 'system', 'content': self.openai_prompt},
                {'role': 'user', 'content': f'{text}. Use the following template: {json.dumps(template)}.'}
            ], format='json')
            result = response['message']['content']
            analysis_file_path = self.get_path('text_analyzer_result.txt')

            self.save_result(analysis_file_path, result)
            self.log(f'3 - Analysis complete. Result is saved to: {analysis_file_path}. Results: {result}')

            return result
        except Exception as e:
            print(f'An error occurred: {e}')
            return None