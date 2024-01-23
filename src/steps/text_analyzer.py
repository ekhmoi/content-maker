from src.steps.base_step import BaseStep

response_defenition = {
    'type': 'function',
    'function': {
        'name':'analyze_text',
        'description': 'Used to analyze text',
        'parameters': {
            'type': 'object',
            'properties': {
                'key_points': {
                    'type': 'array',
                    'items': {
                        'type': 'object',
                        'properties': {
                            'title': { 'type': 'string' },
                            'description': { 'type': 'string' }
                        }
                    }
                }
            }
        }
    }
}

class TextAnalyzer(BaseStep):
    openai_prompt = '''
        Analyze this text and provide key themes and insights with detailed descriptions.
        Return the items in a JSON array.
        Use provided function 'analyze_text' for response.
    '''

    def __init__(self, *args):
        super().__init__('TextAnalyzer', *args)
    
    def execute(self, text: str):
        self.log('3 - Starting analysis of text: ' + text)
        try:
            self.send_message('executing_step', {'step': 3, 'title': self.output_folder})
            response = self.openai.chat.completions.create(
                model='gpt-3.5-turbo-0613',
                messages=[
                    {'role': 'system', 'content': self.openai_prompt},
                    {'role': 'user', 'content': text}
                ],
                tools=[response_defenition],
                tool_choice={ 'type': 'function', 'function': { 'name': 'analyze_text' } },
            )
            
            result = response.choices[0].message.tool_calls[0].function.arguments
            analysis_file_path = self.get_path('text_analyzer_result.txt')

            self.save_result(analysis_file_path, result)
            self.log(f'3 - Analysis complete. Result is saved to: {analysis_file_path}. Results: {result}')

            return result
        except Exception as e:
            print(f'An error occurred: {e}')
            return None