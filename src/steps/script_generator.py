from src.steps.base_step import BaseStep

response_defenition = {
    'type': 'function',
    'function': {
        'name':'generate_script',
        'description': 'Used to generate scripts',
        'parameters': {
            'type': 'object',
            'properties': {
                'script': {
                    'type': 'object',
                    'properties': {
                        'title': { 'type': 'string' },
                        'author': { 'type': 'string' },
                        'genre': { 'type': 'string' },
                        'synopsis': { 'type': 'string' },
                        'characters': {
                            'type': 'array',
                            'items': {
                                'type': 'object',
                                'properties': {
                                    'id': { 'type': 'string' },
                                    'name': { 'type': 'string' },
                                    'description': { 'type': 'string' },
                                    'role': { 'type': 'string' },
                                    'voiceActor': { 'type': 'string' },
                                    'characterDesign': { 'type': 'string' }
                                },
                            }                                            
                        },
                        'scenes': {
                            'type': 'array',
                            'items': {
                                'type': 'object',
                                'properties': {
                                    'id': { 'type': 'string' },
                                    'setting': { 'type': 'string' },
                                    'description': { 'type': 'string' },
                                    'actions': { 
                                        'type': 'array',
                                        'items': {
                                            'type': 'object',
                                            'properties': {
                                                'actionId': { 'type': 'string' },
                                                'characterId': { 'type': 'string' },
                                                'action': { 'type': 'string' },
                                                'dialogue': { 'type': 'string' }
                                            },
                                        }
                                    },
                                    'transitions': { 'type': 'string' }
                                },
                            }
                        },
                        'musicAndSoundEffects': {
                            'type': 'array',
                            'items': {
                                'type': 'object',
                                'properties': {
                                    'sceneId': { 'type': 'string' },
                                    'description': { 'type': 'string' },
                                    'timing': { 'type': 'string' }
                                }
                            }
                        },
                        'additionalNotes': { 'type': 'string' }
                    },
                }
            }
        }
    } 
}

class ScriptGenerator(BaseStep):
    openai_prompt = '''
        Create a script for an animated episode based on this content
        Use provided function 'generate_script' for response.
    '''

    def __init__(self, *args):
        super().__init__('script_generator', *args)
    
    def execute(self, analysis: str):
        self.log('4 - Starting script generation...')
        try:
            response = self.openai.chat.completions.create(
                model='gpt-3.5-turbo-0613',
                messages=[
                    {'role': 'system', 'content': self.openai_prompt},
                    {'role': 'user', 'content': analysis}
                ],
                tools=[response_defenition],
                tool_choice={ 'type': 'function', 'function': { 'name': 'generate_script' } }
            )
            result = response.choices[0].message.tool_calls[0].function.arguments
            result_path = self.get_path('script_generator_result.txt')
            self.save_result(result_path, result)
            self.log(f'4 - Script generation complete - Result is saved to: {result_path}')
            
            return result
        except Exception as e:
            self.log(f'An error occurred: {e}')
            return None
        