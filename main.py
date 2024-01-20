import argparse
from src.content_maker import ContentMaker
from src.websocket_server import WebSocketServer
import os
import subprocess
import threading

def start_frontend():
    # Change directory to the 'ui' folder and start the frontend
    subprocess.run(['npm', 'start'], cwd='ui')

def main():
    # Create a parser
    parser = argparse.ArgumentParser(description="CLI for converting files.")

    # Define the 'convert' command
    parser.add_argument('command', choices=['convert', 'serve'])
    
    # Add arguments for the 'convert' command
    parser.add_argument('-i', '--input', required=False, help='Input file path')
    parser.add_argument('-s', '--step', required=False, help='Step', default='0')
    parser.add_argument('-o', '--output', required=False, help='Output file path')
    parser.add_argument('-k', '--key', required=False, help='Open AI API Key', default=os.environ.get("OPEN_AI_API_KEY"))

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
            # Start the frontend in a separate thread
        frontend_thread = threading.Thread(target=start_frontend)
        frontend_thread.start()
        
        server = WebSocketServer('localhost', 6789)
        server.run()
        

if __name__ == "__main__":
    main()
