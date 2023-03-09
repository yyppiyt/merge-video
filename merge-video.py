import sys, os
from send2trash import send2trash

operation = None
input_path, input_video_extension, input_image_extension = None, None, None
output_path, output_video_extension, merge_list = r"C:\Videos", ".mkv", []

def print_debug_infos():
    print(f"""
Debug infos:
operation: {operation}
input_path: \"{input_path}\", input_video_extension: {input_video_extension}, input_image_extension: {input_image_extension}
output_path: \"{output_path}\", output_video_extension: {output_video_extension}
merge_list:""")
    for x in merge_list:
        print(x)

def press_enter_to_continue(error_message):
    print(f"\n{error_message}")
    input("Press Enter to continue...\n")

# determine what should the program do
def choose_operation():
    global operation
    # if user entered a valid operation, use it
    if len(sys.argv) > 1 and (sys.argv[1] == "merge" or sys.argv[1] == "ytdlp" or sys.argv[1] == "ytarchive"):
        operation = sys.argv[1]
    else:
        while True:
            print("Enter \"1\" for merge video\nEnter \"2\" for yt-dlp(inoperative)\nEnter \"3\" for ytarchive(inoperative)")
            try:
                temp = int(input("Enter number: "))
                if temp >= 1 and temp <= 3:
                    if temp == 1:
                        operation = "merge"
                    elif temp == 2:
                        operation = "ytdlp"
                    elif temp == 3:
                        operation = "ytarchive"
                    else:
                        raise ValueError
                else:
                    raise ValueError
                break
            except ValueError:
                press_enter_to_continue("Incorrect number, enter again")

def change_input_path():
    global input_path, output_path
    while True:
        input_path = input("\nEnter input folder path: ").strip()
        if os.path.isdir(input_path):
            break
        else:
            input_path = None
            press_enter_to_continue("Incorrect path, enter again")

def change_video_extension():
    global input_video_extension
    while True:
        try:
            print("\nEnter \"1\" for .mp4\nEnter \"2\" for .mkv\nEnter \"3\" for .webm\nEnter \"4\" for manual input")
            temp = int(input("Enter number: "))
            if temp >= 1 and temp <= 4:
                if temp == 1:
                    input_video_extension = ".mp4"
                elif temp == 2:
                    input_video_extension = ".mkv"
                elif temp == 3:
                    input_video_extension = ".webm"
                elif temp == 4:
                    break
                else:
                    raise ValueError
            else:
                raise ValueError
            return
        except ValueError:
            press_enter_to_continue("Incorrect number, enter again")
    input_video_extension = input("Manual input video extension: ")
    if input_video_extension[0] != ".":
        input_video_extension = "." + input_video_extension

def change_image_extension():
    global input_image_extension
    while True:
        try:
            print("\nEnter \"1\" for .png\nEnter \"2\" for .jpg\nEnter \"3\" for manual input")
            temp = int(input("Enter number: "))
            if temp >= 1 and temp <= 3:
                if temp == 1:
                    input_image_extension = ".png"
                elif temp == 2:
                    input_image_extension = ".jpg"
                elif temp == 3:
                    break
                else:
                    raise ValueError
            else:
                raise ValueError
            return
        except ValueError:
            press_enter_to_continue("Incorrect number, enter again")
    input_image_extension = input("Manual input image extension: ")
    if input_image_extension[0] != ".":
        input_image_extension = "." + input_image_extension

def update_merge_list():
    global input_video_extension, input_image_extension, merge_list
    temp_video_list, temp_image_list = [], []
    temp_list = os.listdir(input_path)
    for x in temp_list:
        if input_video_extension in x[-len(input_video_extension):]:
            temp_video_list.append(x[:-len(input_video_extension)])
        if input_image_extension in x[-len(input_image_extension):]:
            temp_image_list.append(x[:-len(input_image_extension)])
    # 
    for x in temp_video_list:
        for y in temp_image_list:
            if x == y:
                merge_list.append(x)
                break

def merge_setup():
    change_input_path()
    change_video_extension()
    change_image_extension()
    update_merge_list()

def ytdlp_setup():
    pass

def ytarchive_setup():
    pass

if __name__ == "__main__":
    choose_operation()
    print(f"Selected operation: {operation}")
    if operation == "merge":
        merge_setup()
    elif operation == "ytdlp":
        ytdlp_setup()
    elif operation == "ytarchive":
        ytarchive_setup()
    else:
        sys.exit("\nUnknown operation, program ended")
    # print(os.listdir(input_path))
    
    print_debug_infos()
