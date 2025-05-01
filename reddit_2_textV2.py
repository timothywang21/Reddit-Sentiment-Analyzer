import os
from typing import Tuple
from reddit2text import Reddit2Text
import llm_analyzer
import configparser 

def clear_terminal():
    '''Function that clears terminal every time this script is run'''
    if os.name == 'nt':
        _ = os.system('cls')
        os.system('color')
    else:
        _ = os.system('clear')
def print_fancy_welcome():
    # ANSI escape codes for colors and styles
    BOLD = '\033[1m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    RESET = '\033[0m'

    print(f"\n{BOLD}{RED}╔═{'═' * 55}╗{RESET}")
    print(f"{BOLD}{RED}║ {YELLOW}✨ {CYAN}Reddit Sentiment Program {BLUE}[Powered by Reddit2Text]{YELLOW}✨{RED} ║")
    print(f"{BOLD}{RED}╚═{'═' * 55}╝{RESET}\n")      
def get_reddit_config():
    config = configparser.ConfigParser()
    
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # print(f"Script directory/folder: {script_dir}")
    print(f"Current working directory: {os.getcwd()}")
    
    # Construct the full path to config.ini
    config_path = os.path.join(script_dir, 'config.ini')

    print(f"Attempting to read config from: {config_path}")
    
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"config.ini file not found at {config_path}")
    
    # Actual config read() action!!!
    config.read(config_path) #reading the actual config.ini file
    
    # Check if the config file is read and outputs the sections within the file
    print(f"Successfully read config file from: {config_path}")
    # print(f"Sections in config file: {config.sections()}")  # debug print statement
    
    if 'REDDIT' not in config:
        raise KeyError("'REDDIT' section not found in config file")
    
    return config['REDDIT']


def initialize_reddit2text() -> Reddit2Text:
    """Initialize and return a Reddit2Text instance."""
    
    # returns a reddit_config list already with the ['REDDIT'] entry in it.
    reddit_config = get_reddit_config()
    
    # Creates a Reddit2Text object in order to utlize Reddit2Text library
    return Reddit2Text(
        client_id=reddit_config['client_id'],
        client_secret=reddit_config['client_secret'],
        user_agent=reddit_config['user_agent']
    )

def get_user_input() -> Tuple[str, str, str]: # Tuple type hint is optional here
    """Prompt the user for input and return the URL, output file name, and destination."""
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    RESET = '\033[0m'
    url = input(f"{BOLD}{GREEN}Enter the Reddit URL to analyze: {RESET}")
    output_file = input(f"{BOLD}{YELLOW}Enter the name of the output text file: {RESET}")
    destination = input(f"{BOLD}{CYAN}Enter the destination folder (leave blank for current directory): {RESET}")
    return url, output_file, destination

def get_file_path(output_file: str, destination: str) -> str:
    """Determine the file path based on user input."""
    if not destination:
        destination = os.getcwd()
    return os.path.join(destination, output_file)

def write_to_file(file_path: str, url: str, analysis: str, output: str) -> None:
    """Write the output to a file at the specified path."""
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(f"Original URL: {url}\n\n")
        file.write("[===========SENTIMENT ANALYSIS============]:\n")
        file.write(analysis)
        file.write("\n\n[============REDDIT THREAD CONTENT=============]:\n")
        file.write(output)

def save_all_content(url: str, file_path: str, analysis: str, reddit_content: str):
    """
    Save Reddit content and sentiment analysis to a file.

    Parameters:
    - url: The Reddit URL being analyzed.
    - file_path: The desired file path for saving the output.
    - analysis: The sentiment analysis results.
    - reddit_content: The textual content of the Reddit post/thread.
    """
    try:
        # Ensure the file path ends with ".txt"
        if not file_path.endswith(".txt"):
            file_path += ".txt"

        # Write the content to the specified file
        write_to_file(file_path, url, analysis, reddit_content)
        GREEN = '\033[92m'
        BOLD = '\033[1m'
        RESET = '\033[0m'
        print(f'{BOLD}{GREEN}Output successfully saved to: "{file_path}"{RESET}\n')

    except Exception as e:
        # Handle any errors that occur during the file writing process
        print(f"Error occurred while writing to {file_path}: {e}")

        # Fallback: Save the output to the current working directory
        fallback_path = os.path.join(os.getcwd(), "fallback_output.txt")
        write_to_file(fallback_path, url, analysis, reddit_content)
        print(f"Output saved to fallback location: {fallback_path}\n")

    # Return the Reddit content for further use if needed
    return reddit_content
def print_llm_analysis(analysis) -> (str):
    """Prints the LLM output into a nice and fancy format."""
    # ANSI escape codes for colors and styles
    CYAN = '\033[96m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    WHITE = '\033[97m'
    GREY = '\033[90m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'

    # Extract text content
    text_content = analysis

    # Split content into lines
    lines = text_content.split('\n')

    # Print fancy header
    print(f"\n{BOLD}{BLUE}{'=' * 50}{RESET}")
    print(f"{BOLD}{CYAN}🤖 Analysis Results 🤖{RESET}".center(60))
    print(f"{BOLD}{BLUE}{'=' * 50}{RESET}\n")

    # Print sentiment rating (assuming it's the first line)
    if lines:
        sentiment = lines[0].split(':')
        if len(sentiment) == 2:
            rating = sentiment[1].strip()
            try:
                rating_value = float(rating) # convert string to float value of the rating
                if 0 <= rating_value <= 4:
                    color = RED
                elif 6 <= rating_value <= 10:
                    color = GREEN
                else:
                    color = GREY
            except ValueError:
                color = WHITE  # Default to white if parsing fails
            
            # print(f"{BOLD}{UNDERLINE}Sentiment Rating:{RESET}")
            print(f"{YELLOW}{BOLD}{UNDERLINE}{sentiment[0].strip()}:{RESET} {color}{rating}{RESET}\n")

    # Print analysis content
    print(f"{BOLD}{UNDERLINE}Analysis:{RESET}")
    for line in lines[1:]:
        print(f"{WHITE}{line.strip()}{RESET}")

    # Print fancy footer
    print(f"\n{BOLD}{BLUE}{'=' * 50}{RESET}")
    print(f"{BOLD}{CYAN}End of Analysis{RESET}".center(60))
    print(f"{BOLD}{BLUE}{'=' * 50}{RESET}\n")
    
    return text_content #returns the analyzed text. 
def main():
    import sys
    try:
        # Clear terminal and print welcome message
        clear_terminal()
        print_fancy_welcome()
        
        # Initialize reddit2text library and get user inputs
        r2t = initialize_reddit2text()
        url, output_file, destination = get_user_input()
        file_path = get_file_path(output_file, destination)
        
        # Fetch Reddit content
        reddit_content = r2t.textualize_post(url)
        if not reddit_content:
            print("Error: No content fetched from the provided Reddit URL.")
            sys.exit(1)
        
        # Perform sentiment analysis
        analysis = llm_analyzer.analyze_with_openai(reddit_content)
        if not analysis:
            print("Error: Sentiment analysis failed.")
            sys.exit(1)
        analysis_output = print_llm_analysis(analysis)
        
        # Save Reddit post thread and sentiment analysis
        save_all_content(url, file_path, analysis_output, reddit_content)
        
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
