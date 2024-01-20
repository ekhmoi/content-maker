from src.steps.base_step import BaseStep

class ImageDescriber(BaseStep):
    openai_prompt = """
        Generate a detailed description for this scene
    """

    def __init__(self, output_folder, openai):
        super().__init__('ImageDescriber', output_folder, openai)
        
    def execute(self, script: str):
        """
        Generate detailed scene descriptions from the episode script and save them.
        """
        
        self.log(f'5 - Starting image description generation...')
        scenes = script.split("\n\n")  # Split script into scenes
        image_descriptions = []
        scene_description_path = self.get_path('image_describer_result.txt')

        with open(scene_description_path, 'w', encoding='utf-8') as file:
            for scene in scenes:
                try:
                    response = self.openai.chat.completions.create(
                        model="gpt-3.5-turbo-0613",
                        messages=[
                            {"role": "system", "content": self.openai_prompt},
                            {"role": "user", "content": scene}
                        ]
                    )
                    description = response.choices[0].message.content
                    image_descriptions.append(description)
                    file.write(description + "\n\n")
                except Exception as e:
                    print(f"An error occurred while generating scene description: {e}")

        self.log(f'5 - Image description generation complete - Results are saved to: {scene_description_path}')
        
        return image_descriptions
    