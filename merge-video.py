import subprocess
import sys
import os
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
        print(item)

def press_enter_to_continue(message):
    """Prompt the user to press Enter after displaying a message."""
    input(f"{message}\nPress Enter to continue...")

def get_user_confirmation(prompt):
    """Prompt the user for a yes/no input and return True for 'Y', False for 'N'."""
    while True:
        response = input(prompt).strip().upper()
        if response in ['Y', 'N']:
            return response == 'Y'
        print("Invalid input. Please enter 'Y' or 'N'.")

def create_folder(path):
    """Create a folder at the specified path."""
    try:
        os.makedirs(path, exist_ok=True)
        print(f"Folder created or already exists at: {path}")
        return True
    except Exception as e:
        press_enter_to_continue(f"Error creating folder: {e}")
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
    input_path = get_valid_directory("input")
    output_path = get_valid_directory("output")
    update_merge_list()


if __name__ == "__main__":
    # Check if the user asked for help
    if len(sys.argv) > 1 and sys.argv[1] == "help":
        print("Usage: merge-video [OPTIONS]")
        sys.exit()

    # Check required external components (ffmpeg, mkvmerge)
    check_required_components()

    # Set up paths and merge list
    setup_paths_and_merge_list()

    # Print debug information
    print_debug_info()