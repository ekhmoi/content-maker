import abc
from openai import OpenAI

class BaseStep(abc.ABC):
    
    def __init__(self, openai: OpenAI, step_name: str):
        super().__init__()
        self.openai = openai
        self.step_name = step_name

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
        print(self.step_name + ': ' + message)
    