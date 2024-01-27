import json
from src.steps.base_step import BaseStep

class ImageGenerator(BaseStep):
    def __init__(self, *args):
        super().__init__('image_generator', *args)
        
    def execute(self, image_descriptions: str):
        """
        Generate images for each scene description using DALL-E and save the image URLs.
        """
        self.log('6 - Starting image generation...')
        self.send_message('executing', {'step': 6, 'title': self.output_folder})
        image_urls = []
        image_urls_path = self.get_path("image_generator_result.txt")
        
        image_description_json = json.loads(image_descriptions)
        scenes = image_description_json['scenes']
        
        with open(image_urls_path, 'w', encoding='utf-8') as file:
            for scene in scenes:
                for action in scene['actions']:
                    try:
                        self.log(f'6 - Generation image for action: {action["actionId"]} in scene: {scene["sceneId"]}...')
                        response = self.openai.images.generate(
                            model="dall-e-3",
                            prompt=action['imageDescription'] + '. Generated image should be in a style of Spirited Away',
                            size="1024x1024",
                            quality="standard",
                            n=1,
                        )
                        image_url = response.data[0].url
                        self.send_message('image_generated', {'step': 6, 'title': self.output_folder, 'image_url': image_url})
                        image_urls.append(image_url)
                        file.write(image_url + "\n")
                        self.log(f'6 - Image generation complete: {image_url}')
                    except Exception as e:
                        print(f"An error occurred while generating image: {e}")

        self.log(f'6 - Image generation complete - Results are saved to: {image_urls_path}')
        return image_urls