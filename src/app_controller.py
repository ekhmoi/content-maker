import argparse
from src.content_step_executor import ContentStepExecutor
from src.content_manager import ContentManager
from src.websocket_server import WebSocketServer
from dotenv import load_dotenv
import asyncio
import threading
import os
from queue import Queue

from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import time
import sys

class AppController:
    change_observer = None

    def __init__(self):
        print("App controler")
        load_dotenv()
        self.args = self.get_args()
        self.command_switch = {
            'convert': self.start_convert,
            'serve': self.start_serve
        }

    def get_args(self):
        # Create a parser
        parser = argparse.ArgumentParser(description="CLI for converting files.")
        # Define the 'convert' command
        parser.add_argument('command', choices=['convert', 'serve'])
        # Add arguments for the 'convert' command
        parser.add_argument('-i', '--input', required=False, help='Input file path')
        parser.add_argument('-s', '--step', required=False, help='Step', default='0')
        parser.add_argument('-o', '--output', required=False, help='Output file path')
        parser.add_argument('-p', '--port', required=False, help='Port when running serve command', default='6789')
        parser.add_argument('-k', '--key', required=False, help='Open AI API Key', default=os.getenv("OPEN_AI_API_KEY"))

        return parser.parse_args()


    def process_messages(self, processing_func, server):
        try:
            while True:
                time.sleep(1)
                asyncio.run(processing_func(server))
        except KeyboardInterrupt:
            self.change_observer.stop()
            self.change_observer.join()

    def start(self):
        args = self.get_args()
         # Check if the command is 'convert' and print the parameters
        command = args.command
        command_func = self.command_switch[command]

        if not command_func:
            print(f"Command {command} is not a valid command.")
            return
        
        command_func()
    
    def start_convert(self):
        # Ensure the output directory exists
        if not os.path.exists(self.args.output):
            os.makedirs(self.args.output)

        content_maker = ContentStepExecutor(int(self.args.step), self.args.input, self.args.output, self.args.key, Queue())
        content_maker.execute()

    def start_serve(self):
        content_manager = ContentManager(self.args.output, self.args.key)
        server = WebSocketServer('localhost', int(self.args.port), {
            'get_contents': content_manager.get_contents,
            'get_content_details': content_manager.get_content_details,
            'update_content_details': content_manager.update_content_details,
            'execute_content_step': content_manager.execute_content_step,
            'delete_content': content_manager.delete_content
        })

        message_processing_thread = threading.Thread(target=self.process_messages, args=(content_manager.process_message_queue, server))
        message_processing_thread.start()
        server.run()

    def start_watcher(self):
        patterns = ["*.py"]
        ignore_patterns = None
        ignore_directories = False
        case_sensitive = True
        my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)

        my_event_handler.on_modified = self.on_modified

        path = "."  # Set the directory you want to watch
        self.change_observer = Observer()
        self.change_observer.schedule(my_event_handler, path, recursive=True)
        self.change_observer.start()


    def on_modified(self, event):
        print(f"File {event.src_path} has been modified. Restarting the application.")
        # Restart your application here. You might use os.execv for this.
        os.execv(sys.executable, ['python'] + sys.argv)
