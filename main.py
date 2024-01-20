import argparse
from src.content_maker import ContentMaker


def main():
    # Create a parser
    parser = argparse.ArgumentParser(description="CLI for converting files.")

    # Define the 'convert' command
    parser.add_argument('command', choices=['convert'])
    
    # Add arguments for the 'convert' command
    parser.add_argument('-i', '--input', required=True, help='Input file path')
    parser.add_argument('-o', '--output', required=True, help='Output file path')
    parser.add_argument('-k', '--key', required=False, help='Open AI API Key')

    # Parse arguments
    args = parser.parse_args()

    # Check if the command is 'convert' and print the parameters
    if args.command == 'convert':
        content_maker = ContentMaker(args.input, args.output, args.key)
        content_maker.execute()

if __name__ == "__main__":
    main()
