import sys, os
from send2trash import send2trash

operation = None
input_path, input_video_extension, input_image_extension = None, None, None
output_path, output_video_extension, merge_list = r"C:\Videos", ".mkv", []


def print_debug_infos():
    print(
        f"""
Debug infos:
operation: {operation}
input_path: \"{input_path}\", input_video_extension: {input_video_extension}, input_image_extension: {input_image_extension}
output_path: \"{output_path}\", output_video_extension: {output_video_extension}
merge_list:"""
    )
    for i in merge_list:
        print(i)


def press_enter_to_continue(error_message):
    print(f"\n{error_message}")
    input("Press Enter to continue...\n")


# Determine what should the program do
def choose_operation():
    global operation
    # If user entered a valid operation, use it
    if len(sys.argv) > 1 and sys.argv[1] == "merge":
        operation = sys.argv[1]
    else:
        while True:
            # print("Enter \"1\" for merge video\nEnter \"2\" for yt-dlp(inoperative)\nEnter \"3\" for ytarchive(inoperative)")
            print('Enter "1" for merge video')
            try:
                temp = int(input("Enter number: "))
                if temp >= 1 and temp <= 3:
                    match temp:
                        case 1:
                            operation = "merge"
                        # case 2:
                        #     operation = "ytdlp"
                        # case 3:
                        #     operation = "ytarchive"
                        case _:
                            raise ValueError
                else:
                    raise ValueError
                break
            except ValueError:
                press_enter_to_continue("Incorrect number, enter again")


def change_path(operation=None):
    global input_path, output_path
    match operation:
        case "input":
            printString = "\nEnter input folder path: "
        case "output":
            printString = "\nEnter output folder path: "
        case _:
            sys.exit("\nUnknown operation while changing path, program ended")
    while True:
        temp_path = input(printString).strip()
        if os.path.isdir(temp_path):
            while temp_path[-1:] == ".":
                temp_path = temp_path[:-1]
            break
        else:
            temp_path = None
            press_enter_to_continue("Incorrect path, enter again")
    if operation == "input":
        input_path = temp_path
    elif operation == "output":
        output_path = temp_path


# def change_input_path():
#     global input_path
#     while True:
#         input_path = input("\nEnter input folder path: ").strip()
#         if os.path.isdir(input_path):
#             while input_path[-1:] == ".":
#                 input_path = input_path[:-1]
#             break
#         else:
#             input_path = None
#             press_enter_to_continue("Incorrect path, enter again")


# def change_output_path():
#     global output_path
#     while True:
#         output_path = input("\nEnter output folder path: ").strip()
#         if os.path.isdir(output_path):
#             while output_path[-1:] == ".":
#                 output_path = output_path[:-1]
#             break
#         else:
#             output_path = None
#             press_enter_to_continue("Incorrect path, enter again")


def change_extension(operation):
    global input_video_extension, input_image_extension
    match operation:
        case "video":
            print(
                '\nEnter "1" for .mp4\nEnter "2" for .mkv\nEnter "3" for .webm\nEnter "4" for manual input'
            )
        case "image":
            print(
                '\nEnter "1" for .png\nEnter "2" for .jpg\nEnter "3" for manual input'
            )
        case _:
            sys.exit("\nUnknown operation while changing extension, program ended")
    while True:
        try:
            index = int(input("Enter number: "))
            match operation:
                case "video":
                    match index:
                        case 1:
                            input_video_extension = ".mp4"
                        case 2:
                            input_video_extension = ".mkv"
                        case 3:
                            input_video_extension = ".webm"
                        case 4:
                            break
                        case _:
                            raise ValueError
                case "image":
                    match index:
                        case 1:
                            input_image_extension = ".png"
                        case 2:
                            input_image_extension = ".jpg"
                        case 3:
                            break
                        case _:
                            raise ValueError
            return
        except ValueError:
            press_enter_to_continue("Incorrect number, enter again")
    user_input_extension = input("Manual input extension: ")
    if user_input_extension[0] != ".":
        user_input_extension = "." + user_input_extension
    match operation:
        case "video":
            input_video_extension = user_input_extension
        case "image":
            input_image_extension = user_input_extension


# def change_video_extension():
#     global input_video_extension
#     while True:
#         try:
#             print(
#                 '\nEnter "1" for .mp4\nEnter "2" for .mkv\nEnter "3" for .webm\nEnter "4" for manual input'
#             )
#             temp = int(input("Enter number: "))
#             if temp >= 1 and temp <= 4:
#                 if temp == 1:
#                     input_video_extension = ".mp4"
#                 elif temp == 2:
#                     input_video_extension = ".mkv"
#                 elif temp == 3:
#                     input_video_extension = ".webm"
#                 elif temp == 4:
#                     break
#                 else:
#                     raise ValueError
#             else:
#                 raise ValueError
#             return
#         except ValueError:
#             press_enter_to_continue("Incorrect number, enter again")
#     input_video_extension = input("Manual input video extension: ")
#     if input_video_extension[0] != ".":
#         input_video_extension = "." + input_video_extension


# def change_image_extension():
#     global input_image_extension
#     while True:
#         try:
#             print(
#                 '\nEnter "1" for .png\nEnter "2" for .jpg\nEnter "3" for manual input'
#             )
#             temp = int(input("Enter number: "))
#             if temp >= 1 and temp <= 3:
#                 if temp == 1:
#                     input_image_extension = ".png"
#                 elif temp == 2:
#                     input_image_extension = ".jpg"
#                 elif temp == 3:
#                     break
#                 else:
#                     raise ValueError
#             else:
#                 raise ValueError
#             return
#         except ValueError:
#             press_enter_to_continue("Incorrect number, enter again")
#     input_image_extension = input("Manual input image extension: ")
#     if input_image_extension[0] != ".":
#         input_image_extension = "." + input_image_extension


def update_merge_list():
    global input_video_extension, input_image_extension, merge_list
    temp_video_list, temp_image_list = [], []
    temp_list = os.listdir(input_path)
    for i in temp_list:
        if i.endswith(input_video_extension):
            temp_video_list.append(i[: -len(input_video_extension)])
        if i.endswith(input_image_extension):
            temp_image_list.append(i[: -len(input_image_extension)])
    #
    for i in temp_video_list:
        for j in temp_image_list:
            if i == j:
                merge_list.append(i)
                break


def merge_setup():
    change_path("input")
    change_path("output")
    change_extension("video")
    change_extension("image")
    update_merge_list()


def ytdlp_setup():
    print("ytdlp_setup()")
    sys.exit()


def ytarchive_setup():
    print("ytarchive_setup()")
    sys.exit()


if __name__ == "__main__":
    choose_operation()
    print(f"Selected operation: {operation}")

    match operation:
        case "merge":
            merge_setup()
        case "ytdlp":
            ytdlp_setup()
        case "ytarchive":
            ytarchive_setup()
        case _:
            sys.exit("\nUnknown operation, program ended")

    # if operation == "merge":
    #     merge_setup()
    # elif operation == "ytdlp":
    #     ytdlp_setup()
    # elif operation == "ytarchive":
    #     ytarchive_setup()
    # else:
    #     sys.exit("\nUnknown operation, program ended")
    # print(os.listdir(input_path))

    print_debug_infos()
