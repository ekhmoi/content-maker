import os

from src.steps.base_step import BaseStep

class ImageDescriber(BaseStep):
    openaiPrompt = """
        Generate a detailed description for this scene
    """
    def __init__(self, openai):
        super().__init__(openai, 'ImageDescriber')
    
    def execute(self, script: str, output_folder: str, original_file_name: str):
        """
        Generate detailed scene descriptions from the episode script and save them.
        """
        
        self.log('Starting image description generation...')
        scenes = script.split("\n\n")  # Split script into scenes
        image_descriptions = []
        scene_description_path = os.path.join(output_folder, f"{original_file_name}-images-descriptions.txt")

        with open(scene_description_path, 'w', encoding='utf-8') as file:
            for scene in scenes:
                try:
                    response = self.openai.chat.completions.create(
                        model="gpt-3.5-turbo-0613",
                        messages=[
                            {"role": "system", "content": self.openaiPrompt},
                            {"role": "user", "content": scene}
                        ]
                    )
                    description = response.choices[0].message.content
                    image_descriptions.append(description)
                    file.write(description + "\n\n")
                except Exception as e:
                    print(f"An error occurred while generating scene description: {e}")

        self.log('Image description generation complete. Results are saved to ' + scene_description_path)
        
        return image_descriptions
    