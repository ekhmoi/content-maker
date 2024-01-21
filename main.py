import argparse
from src.content_maker import ContentMaker
from src.content_manager import ContentManager
from src.websocket_server import WebSocketServer
from dotenv import load_dotenv

import os

from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import time
import sys

my_observer = None

def on_modified(event):
    print(f"File {event.src_path} has been modified. Restarting the application.")
    # Restart your application here. You might use os.execv for this.
    os.execv(sys.executable, ['python'] + sys.argv)

def start_watcher():
    patterns = ["*.py"]
    ignore_patterns = None
    ignore_directories = False
    case_sensitive = True
    my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)

    my_event_handler.on_modified = on_modified

    path = "."  # Set the directory you want to watch
    my_observer = Observer()
    my_observer.schedule(my_event_handler, path, recursive=True)
    my_observer.start()

def main():
    load_dotenv()
    print('key' ,os.getenv("OPEN_AI_API_KEY"))
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

    # Parse arguments
    args = parser.parse_args()

    # Check if the command is 'convert' and print the parameters
    if args.command == 'convert':
        # Ensure the output directory exists
        if not os.path.exists(args.output):
            os.makedirs(args.output)

        content_maker = ContentMaker(int(args.step), args.input, args.output, args.key)
        content_maker.execute()
        
    elif args.command == 'serve':
        content_manager = ContentManager(args.output, args.key)
        server = WebSocketServer('localhost', int(args.port), {
            'get_contents': content_manager.get_contents,
            'get_content_details': content_manager.get_content_details,
            'update_content_details': content_manager.update_content_details,
            'execute_content_step': content_manager.execute_content_step,
            'download_content_from_youtube': content_manager.download_content_from_youtube,
            'delete_content': content_manager.delete_content
        })
        server.run()
         # Add this at the end of your main function to keep the script running
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            my_observer.stop()
            my_observer.join()
        

if __name__ == "__main__":
    start_watcher()  # Start the watcher
    main()