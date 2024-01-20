
import os

from src.steps.base_step import BaseStep

class ImageGenerator(BaseStep):
    def __init__(self, openai):
        super().__init__(openai, 'ImageGenerator')
    
    def execute(self, image_descriptions: str, output_folder: str, original_file_name: str):
        """
        Generate images for each scene description using DALL-E and save the image URLs.
        """
        self.log('Starting image generation...')
        image_urls = []
        image_urls_path = os.path.join(output_folder, f"{original_file_name}-image-urls.txt")

        with open(image_urls_path, 'w', encoding='utf-8') as file:
            for description in image_descriptions:
                try:
                    response = self.openai.images.generate(
                        model="dall-e-3",
                        prompt=description,
                        size="1024x1024",
                        quality="standard",
                        n=1,
                    )
                    image_url = response.data[0].url
                    image_urls.append(image_url)
                    file.write(image_url + "\n")
                except Exception as e:
                    print(f"An error occurred while generating image: {e}")
        self.log('Image generation complete. Results are saved to'+ image_urls_path)
        return image_urls