import sys, os
operation, input_path, output_path, input_video_extension, output_extension = None, None, r"C:\Videos", None, "mkv"

def press_enter_to_continue(error_message):
    print(f"\n{error_message}")
    input("Press Enter to continue...\n")

def choose_operation():
    global operation
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
        input_path = input("Enter input folder path: ").strip()
        if os.path.isdir(input_path):
            break
        else:
            input_path = None
            press_enter_to_continue("Incorrect path, enter again")
    # print(f"Input location: {input_path}")
    # print(f"Default output location: {output_path}")

def change_video_extension():
    global input_video_extension
    while True:
        try:
            print("Enter \"1\" for mp4\nEnter \"2\" for mkv\nEnter \"3\" for webm\nEnter \"4\" for manual input")
            temp = int(input("Enter number: "))
            if temp >= 1 and temp <= 4:
                if temp == 1:
                    input_video_extension = "mp4"
                elif temp == 2:
                    input_video_extension = "mkv"
                elif temp == 3:
                    input_video_extension = "webm"
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

def merge_setup():
    change_input_path()
    change_video_extension()
                    
def ytdlp_setup():
    pass
                
def ytarchive_setup():
    pass
                
if __name__ == "__main__":
    # choose_operation()
    # print(f"Selected operation: {operation}")
    # if operation == "merge":
    #     merge_setup()
    # elif operation == "ytdlp":
    #     ytdlp_setup()
    # elif operation == "ytarchive":
    #     ytarchive_setup()
    # else:
    #     sys.exit("\nUnknown operation, program ended")
    change_video_extension()
