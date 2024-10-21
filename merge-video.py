import subprocess
import sys
import os
import re
from pathlib import Path
from send2trash import send2trash

# Constants for file extensions
VIDEO_EXTENSIONS = ["mkv", "mp4", "webm"]
IMAGE_EXTENSIONS = ["png", "jpg"]
OUTPUT_VIDEO_EXTENSION = "mkv"

# Global variables
input_path = None
output_path = None
merge_list = []
complete_counter = 0
warning_counter = 0
abort_counter = 0

def print_debug_info():
    """Prints debug information about paths and the merge list."""
    print(f"""
Debug Info:
Input Path: \"{input_path}\"
Video Extensions: {VIDEO_EXTENSIONS}
Image Extensions: {IMAGE_EXTENSIONS}
Output Path: \"{output_path}\"
Output Video Extension: {OUTPUT_VIDEO_EXTENSION}
Merge List:""")
    for item in merge_list:
        print(f"{item}, Channel name: {get_channel_name(item[0])}")

def press_enter_to_continue(message):
    """Prompt the user to press Enter after displaying a message."""
    input(f"{message}\nPress Enter to continue...")

def get_user_confirmation(prompt, list_all=False):
    """Prompt the user for a yes/no input and return True for 'Y', False for 'N'."""
    while True:
        response = input(prompt).strip().upper()
        if response == 'LIST' and list_all:
            for item in merge_list:
                print(item[0])
            continue
        elif response in ['Y', 'N']:
            return response == 'Y'
        print("Invalid input. Please enter 'Y' or 'N'.")

def create_folder(path):
    """Create a folder at the specified path."""
    try:
        os.makedirs(path, exist_ok=True)
        print(f"Folder created or already exists at: {path}")
        return True
    except Exception as e:
        print(f"Error creating folder: {e}")
        return False

def prompt_folder_creation(path):
    """Prompt the user to create a folder if it doesn't exist."""
    if get_user_confirmation("Folder not found, create? [Y/N] "):
        return create_folder(path)
    else:
        print("Folder creation aborted.")
        return False

def check_required_components():
    """Check for required external components (ffmpeg, mkvmerge) and exit if missing."""
    components = ["ffmpeg", "mkvmerge"]
    missing_components = []

    for component in components:
        result = subprocess.run(["where", component], capture_output=True, text=True)
        if result.returncode != 0:
            missing_components.append(f"{component} not found: {result.stderr.strip()}")

    if missing_components:
        print("\n".join(missing_components))
        sys.exit("Missing one or more required components. Program exited.")

def get_valid_directory(operation):
    """Prompt the user for a valid directory path (input or output)."""
    prompt_message = f"\nEnter {'output' if operation == 'output' else 'input'} folder path: "
    while True:
        path = input(prompt_message).strip().rstrip(".")
        if os.path.isdir(path):
            return path
        elif operation == "output" and prompt_folder_creation(path):
            return path
        else:
            press_enter_to_continue("Invalid path, please enter a correct directory.")

def update_merge_list():
    """Update the merge list with matching video, image, and optional description files from the input directory."""
    global merge_list
    directory_path = Path(input_path)
    file_map = {}

    # Collect files and group them by their name (stem)
    for file in directory_path.iterdir():
        if file.is_file():
            name = file.stem  # Get the file name without extension
            extension = file.suffix.lstrip('.')  # Get the file extension without the dot
            file_map.setdefault(name, []).append(extension)

    # Find matching video, image, and optional description files
    for name, extensions in file_map.items():
        video_ext = next((ext for ext in VIDEO_EXTENSIONS if ext in extensions), None)
        image_ext = next((ext for ext in IMAGE_EXTENSIONS if ext in extensions), None)
        description_ext = "description" if "description" in extensions else None

        # Append to merge_list if both video and image extensions are found
        if video_ext and image_ext:
            merge_item = (name, video_ext, image_ext)
            if description_ext:
                merge_item += (description_ext,)  # Add description if found
            merge_list.append(merge_item)

def setup_paths_and_merge_list():
    """Set up the input and output paths and update the merge list."""
    global input_path, output_path
    if len(sys.argv) > 1:
        for arg in sys.argv:
            if os.path.isdir(arg) and input_path is None:
                input_path = arg
                print(f"Input folder path: {input_path}")
            elif os.path.isdir(arg) and output_path is None:
                output_path = arg
                print(f"Output folder path: {output_path}")
    if input_path is None: input_path = get_valid_directory("input")
    if output_path is None: output_path = get_valid_directory("output")
    update_merge_list()

def get_mkvmerge_command(item):
    name = item[0]
    video_ext = item[1]
    image_ext = item[2]
    subtitle_string = ''
    attachment_string = ''
    track_order_string = "0:0,0:1"
    if len(item) > 3:
        for attachment in item[3:]:
            attachment_string += f"--attach-file \"{input_path}/{name}.{attachment}\" "
    return f'mkvmerge --output "{output_path}/{get_channel_name(name)}/{name}.{OUTPUT_VIDEO_EXTENSION}" ' \
           f'"{input_path}/{name}.{video_ext}" ' \
           f'{subtitle_string} ' \
           f'--attachment-name cover.{image_ext} ' \
           f'--attach-file "{input_path}/{name}.{image_ext}" ' \
           f'{attachment_string} ' \
           f'--track-order {track_order_string}'

def run_mkvmerge(item):
    # print(get_mkvmerge_command(item))
    # Start the subprocess
    mkvmerge = subprocess.Popen(
        get_mkvmerge_command(item),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,
        encoding='utf-8'
    )
    
    for line in mkvmerge.stdout:
        if re.search(r':.*%\s*$', line):  # Regex to match : followed by any text and %
            print(f"\r{line.strip()}", end='')  # Update the line
            sys.stdout.flush()  # Ensure immediate output
        else:
            print(line, end='')
    return mkvmerge.wait()

def merge():
    global complete_counter, warning_counter, abort_counter
    if len(merge_list) < 1:
        sys.exit("Found 0 files to be merge. Program exited.")
    if get_user_confirmation(f"Enter \"List\" to list all file\nFound {len(merge_list)} files to be merge, continue? [Y/N] ", True):
        for item in merge_list:
            result = run_mkvmerge(item)
            if result == 0:
                complete_counter += 1
            elif result == 1:
                warning_counter += 1
            elif result == 2:
                abort_counter += 1
            print(f"{len(merge_list) - complete_counter - warning_counter - abort_counter} file(s) remaining\n")
        print(f"Merge process ended with {complete_counter} video completed, {warning_counter} warning, {abort_counter} error" \
              f"{"\nWarning occurred, check both the warning and the resulting file is recommended" if warning_counter else ""}" \
              f"{"\nError occurred, some missions are aborted" if abort_counter else ""}")
    else:
        sys.exit("Merge aborted. Program exited.")

def get_channel_name(text):
    # Regular expression to find all occurrences of text within square brackets
    matches = re.findall(r'\[(.*?)\]', text)
    # Return the last match, if any
    return matches[-1] if matches else None

if __name__ == "__main__":
    # Check if the user asked for help
    if len(sys.argv) > 1 and sys.argv[1] == "help":
        print("Usage: merge-video [OPTIONS] SOURCE_FOLDER OUTPUT_FOLDER")
        sys.exit()

    # Check required external components (ffmpeg, mkvmerge)
    check_required_components()

    # Set up paths and merge list
    setup_paths_and_merge_list()

    # Print debug information
    # print_debug_info()

    merge()