import os

class ContentManager:
    def __init__(self):
        self.base_path = './outputs/'
        print("This is Content Manager")

    def get_contents(self, data):
        content_list = []

        # Check if base_path exists and is a directory
        if os.path.exists(self.base_path) and os.path.isdir(self.base_path):
            # Iterate through each item in the base_path
            for item in os.listdir(self.base_path):
                item_path = os.path.join(self.base_path, item)
                # Check if the item is a directory
                if os.path.isdir(item_path):
                    folder_contents = {
                        'folder_name': item,
                        'file_names': [f for f in os.listdir(item_path) if os.path.isfile(os.path.join(item_path, f))]
                    }
                    content_list.append(folder_contents)

        return content_list
    
    def get_content_details(self, folder_name):
        folder_path = os.path.join(self.base_path, folder_name)
        content_details = {'folder_name': folder_name}

        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            for file_name in os.listdir(folder_path):
                file_path = os.path.join(folder_path, file_name)
                if os.path.isfile(file_path) and file_name != 'input.wav':
                    with open(file_path, 'r') as file:
                        content_details[file_name] = file.read()
        return content_details