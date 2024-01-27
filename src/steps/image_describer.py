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
        }
    }
}

class ImageDescriber(BaseStep):
    openai_prompt = "Using the provided 'script' JSON object, generate comprehensive and vivid descriptions for each key action within each scene. Each description should paint a clear and detailed picture suitable for image creation. Focus on character appearances, expressions, and movements, the specific setting of the scene, and any important props or background elements. Incorporate the overall genre, mood, and synopsis of the script to ensure that each description aligns with the story's tone and context. Utilize the 'describe_image' function for formatting the responses."

    def __init__(self, *args):
        super().__init__('image_describer', *args)
        
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
    