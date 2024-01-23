import abc
import json
from openai import OpenAI
import os
from queue import Queue

class BaseStep(abc.ABC):
    
    def __init__(self, step_name: str, output_folder: str,  openai: OpenAI, queue: Queue, metadata: any):
        super().__init__()
        self.openai = openai
        self.output_folder = output_folder
        self.step_name = step_name
        self.queue = queue
        self.metadata = metadata

    @abc.abstractmethod
    def execute(self):
        pass

    def save_result(self, path, body):
        with open(path, 'w', encoding='utf-8') as output_file:
            output_file.write(body)
            
    def read_file(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return content
    
    def log(self, message):
        print('[' + self.step_name + ']: ' + message)

    def get_path(self, file_name: str):
        return os.path.join(self.output_folder, file_name)
    
    def send_message(self, command: str, data: any):
        self.queue.put((command, data))
        
    def update_metadata(self, key: str, data: any):
        self.metadata[key] = data
        with open(self.output_folder + '/metadata.json', 'w', encoding='utf-8') as output_file:
            output_file.write(json.dumps(self.metadata))
    
    def get_metadata(self):
        return self.metadata[self.step_name]