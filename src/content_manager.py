import os
import shutil
from src.content_maker import ContentMaker
from src.steps.input_converter import InputConverter
import threading

def execute_content_step_thread(output_folder, data, openai_api_key):
    """
    This method takes the data dictionary and runs the ContentMaker from given data['step'] with given data['input']
    data: {
        step: number
        input: string
    }
    """
    
    # Create ContentMaker instance

    orderedStepName = [
        'input.wav',
        'audio_transcriber_result.txt',
        'text_analyzer_result.txt',
        'script_generator_result.txt',
        'image_describer_result.txt',
        'image_generator_result.txt',
    ]
    output_folder = f"{output_folder}/{data['folder_name']}"
    step = int(data['step'])
    input_path = f'{output_folder}/{orderedStepName[step]}'
    content_maker = ContentMaker(step, input_path, output_folder, openai_api_key)
    
    # Execute the ContentMaker
    content_maker.execute()
    
    # Return the results
    return content_maker.results

class ContentManager:
    def __init__(self, output_folder, openai_api_key):
        self.output_folder = output_folder
        self.openai_api_key = openai_api_key
        print("This is Content Manager")

    def get_contents(self, data):
        content_list = []
        print("DASHSHAGH", self.output_folder)
        # Check if output_folder exists and is a directory
        if os.path.exists(self.output_folder) and os.path.isdir(self.output_folder):
            # Iterate through each item in the output_folder
            for item in os.listdir(self.output_folder):
                item_path = os.path.join(self.output_folder, item)
                # Check if the item is a directory
                if os.path.isdir(item_path):
                    folder_contents = {
                        'folder_name': item,
                        'file_names': [f for f in os.listdir(item_path) if os.path.isfile(os.path.join(item_path, f))]
                    }
                    content_list.append(folder_contents)

        return content_list
    
    def get_content_details(self, folder_name):
        folder_path = os.path.join(self.output_folder, folder_name)
        content_details = {'folder_name': folder_name}

        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            for file_name in os.listdir(folder_path):
                file_path = os.path.join(folder_path, file_name)
                if os.path.isfile(file_path) and file_name != 'input.wav':
                    with open(file_path, 'r') as file:
                        content_details[file_name] = file.read()
        return content_details
    
    def update_content_details(self, data):
        """
        This method takes the data dictionary and updates the files under self.output_folder / data['folder_name']
        data: {
            folder_name: string
            updates: [
            {file_name: string, content: string}
            ]
        }
        """
        # print("dash", data)
        folder_path = os.path.join(self.output_folder, data['folder_name'])
        
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            for update in data['updates']:
                file_path = os.path.join(folder_path, update['file_name'])
                with open(file_path, 'w') as file:
                    file.write(update['content'])

   
    
    def execute_content_step(self, data):
        # This method starts a new thread
        thread = threading.Thread(target=execute_content_step_thread, args=(self.output_folder, data, self.openai_api_key))
        thread.start()
        # Optionally, you can return the thread if you want to join it or check its status later
        return {
            'Status': 'done'
        }
    
    def download_content_from_youtube(self, data):
        output_folder = f"{self.output_folder}/{data['folder_name']}"
        youtube_downloader = InputConverter(output_folder, None)
        youtube_downloader.execute(data['youtube_url'])

        return f'{output_folder}/input.wav'


    def delete_content(self, data):
        """
        Delete folder under f"{self.output_folder}/{data['folder_name']}"
        """
        folder_path = os.path.join(self.output_folder, data['folder_name'])
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            shutil.rmtree(folder_path)
