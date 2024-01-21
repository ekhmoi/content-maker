from src.steps.base_step import BaseStep
import json

response_defenition = {
    'type': 'function',
    'function': {
        'name':'describe_image',
        'description': 'Used to create description for the image',
        'parameters': {
            'type': 'object',
            'properties': {
                'script': {
                    'type': 'object',
                    'properties': {
                        'title': { 'type': 'string' },
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
                                },
                            }
                        },
                        'scenes': {
                            'type': 'array',
                            'items': {
                                'type': 'object',
                                'properties': {
                                    'sceneId': { 'type': 'string' },
                                    'actions': {
                                        'type': 'array',
                                        'items': {
                                            'type': 'object',
                                            'properties': {
                                                'actionId': { 'type': 'string' },
                                                'imageDescription': { 
                                                    'type': 'string',
                                                    'description':'Detailed description of the action'
                                                }
                                            }
                                        }
                                    },
                                }
                            }
                        },
                    }
                },
            }
        }
    }
}

class ImageDescriber(BaseStep):
    openai_prompt = """
        Generate a detailed description for the each 'action' of the each item in 'scenes' in provided 'script' JSON object.
        The description should be detailed enough to draw an image of the action.
        Use provided function 'describe_image' for response.
    """

    def __init__(self, output_folder, openai):
        super().__init__('ImageDescriber', output_folder, openai)
        
    def execute(self, script: str):
        """
        Generate detailed scene descriptions from the episode script and save them.
        """
        
        self.log(f'5 - Starting image description generation...')
        image_descriptions = []
        scene_description_path = self.get_path('image_describer_result.txt')

        with open(scene_description_path, 'w', encoding='utf-8') as file:            
            try:
                response = self.openai.chat.completions.create(
                    model="gpt-3.5-turbo-0613",
                    messages=[
                        {"role": "system", "content": self.openai_prompt},
                        {"role": "user", "content": script}
                    ],
                    tools=[response_defenition],
                    tool_choice={ 'type': 'function', 'function': { 'name': 'describe_image' } }
                )
                description = response.choices[0].message.tool_calls[0].function.arguments
                image_descriptions.append(description)
                file.write(description + "\n\n")
            except Exception as e:
                print(f"An error occurred while generating scene description: {e}")

        self.log(f'5 - Image description generation complete - Results are saved to: {scene_description_path}')
        
        return image_descriptions
    