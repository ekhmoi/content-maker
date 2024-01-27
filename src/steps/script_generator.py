from src.steps.base_step import BaseStep
import ollama

class ScriptGenerator(BaseStep):
    llm_prompt = '''
        Create a script for an animated episode based on this content.
        Return response in a JSON object with the following format:
        {
            "title": "The title of the episode",
            "author": "The name of the author",
            "genre": "The genre of the episode",
            "synopsis": "A brief synopsis of the episode",
            "characters": [
                {
                    "id": "The id of the character",
                    "name": "The name of the character",
                    "description": "A brief description of the character",
                    "role": "The role of the character in the episode",
                    "voiceActor": "The name of the voice actor",
                    "characterDesign": "The name of the character design"
                }
            ],
            "scenes": [
                {
                    "id": "The id of the scene",
                    "setting": "The setting of the scene",
                    "description": "A brief description of the scene",
                    "actions": [
                        {
                            "actionId": "The id of the action",
                            "characterId": "The id of the character",
                            "action": "The action of the character",
                            "dialogue": "The dialogue of the character"
                        }
                    ],
                    "transitions": "The transition of the scene"
                }
            ],
            "musicAndSoundEffects": [
                {
                    "sceneId": "The id of the scene",
                    "description": "A brief description of the scene",
                    "timing": "The timing of the scene"
                }
            ],
            "additionalNotes": "Any additional notes"
        }
    '''

    def __init__(self, *args):
        super().__init__('script_generator', *args)
    
    def execute(self, analysis: str):
        self.log('4 - Starting script generation...')
        try:
            response = ollama.chat(model='llama2', messages=[
                {'role': 'system', 'content': self.llm_prompt},
                {'role': 'user', 'content': analysis}
            ], format='json')
            result = response['message']['content']            
            result_path = self.get_path('script_generator_result.txt')
            
            self.save_result(result_path, result)
            self.log(f'4 - Script generation complete - Result is saved to: {result_path}')
            
            return result
        except Exception as e:
            self.log(f'An error occurred: {e}')
            return None
        