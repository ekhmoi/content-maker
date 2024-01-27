from src.steps.base_step import BaseStep
import ollama

class ImageDescriber(BaseStep):
    llm_prompt = ''' 
        Using the provided 'script' JSON object, generate comprehensive and 
        vivid descriptions for each key action within each scene. 
        Each description should paint a clear and detailed picture suitable for image creation. 
        Focus on character appearances, expressions, and movements, 
        the specific setting of the scene, and any important props or background elements. 
        Incorporate the overall genre, mood, and synopsis of the script to ensure
        that each description aligns with the story's tone and context. 
        Return response in a JSON object with the following format:
        {
            "scenes": [
                {
                    "sceneId": "The id of the scene",
                    "actions": [
                        {
                            "actionId": "The id of the action",
                            "imageDescription": "The detailed description of the action"
                        }
                    ]
                }
            ]
        }
    ''' 

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
                response = ollama.chat(model='llama2', messages=[
                    {'role': 'system', 'content': self.llm_prompt},
                    {'role': 'user', 'content': script}
                ], format='json')
                description = response['message']['content']            
                
                image_descriptions.append(description)
                file.write(description + "\n\n")
            except Exception as e:
                print(f"An error occurred while generating scene description: {e}")

        self.log(f'5 - Image description generation complete - Results are saved to: {scene_description_path}')
        
        return image_descriptions
    