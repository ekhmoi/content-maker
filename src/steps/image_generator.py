from src.steps.base_step import BaseStep

class ImageGenerator(BaseStep):
    def __init__(self, output_folder, openai):
        super().__init__('ImageGenerator', output_folder, openai)
        
    def execute(self, image_descriptions: str):
        """
        Generate images for each scene description using DALL-E and save the image URLs.
        """
        self.log('6 - Starting image generation...')
        image_urls = []
        image_urls_path = self.get_path("image_generator_result.txt")

        with open(image_urls_path, 'w', encoding='utf-8') as file:
            for description in image_descriptions:
                try:
                    response = self.openai.images.generate(
                        model="dall-e-3",
                        prompt=description,
                        size="256x256",
                        quality="standard",
                        n=1,
                    )
                    image_url = response.data[0].url
                    image_urls.append(image_url)
                    file.write(image_url + "\n")
                except Exception as e:
                    print(f"An error occurred while generating image: {e}")
        self.log(f'6 - Image generation complete - Results are saved to: {image_urls_path}')
        return image_urls