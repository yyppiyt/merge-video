import sys
operation = None

def chooseOperation():
    global operation
    if len(sys.argv) > 1 and (sys.argv[1] == "merge" or sys.argv[1] == "ytdlp" or sys.argv[1] == "ytarchive"):
        operation = sys.argv[1]
    else:
        while True:
            print("Enter \"1\" for merge video\nEnter \"2\" for yt-dlp(inoperative)\nEnter \"3\" for ytarchive(inoperative)")
            try:
                operation = int(input("Enter number: "))
                if operation >= 1 or operation <= 3:
                    if operation == 1:
                        operation = "merge"
                    elif operation == 2:
                        operation = "ytdlp"
                    elif operation == 3:
                        operation = "ytarchive"
                    else:
                        raise ValueError
                else:
                    raise ValueError
                break
            except ValueError:
                print("\nIncorrect number, enter again")
                input("Press Enter to continue...\n")
    print(f"Selected operation: {operation}")
                
if __name__ == "__main__":
    # print(f"sys.argv: {sys.argv}")
    # print(f"len(sys.argv): {len(sys.argv)}\n")
    chooseOperation()
    

