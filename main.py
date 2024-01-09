from tkinter import *
import random
import time

window = Tk()

sentences = open("sentences.txt", mode="r").read().split("\n")
prev_line = ""
user_line = ""
end_of_typing = False
starting_time = 0
beginning_time = 0
all_speeds = []
reset_timer = 0


# Function to assign randomly picked sentence to user
def assign_sentence(arr_line):
    global prev_line
    line = random.choice(arr_line)
    if prev_line == line:
        line = random.choice(arr_line)
    prev_line = line
    return line


# function to calculate speed of user when starts typing
def start_calculating(event):
    global starting_time, beginning_time,reset_timer,end_of_typing, user_line, text_to_display

    if end_of_typing:
        print("Can't type further")
        return

    if starting_time == 0:
        starting_time = time.time()
    if beginning_time == 0:
        beginning_time = time.time()

    if event.keysym == "Backspace":
        user_line = user_line[0: len(user_line)-1]
        starting_time = time.time()
        return
    else:
        user_line += event.char
        end_time = time.time()
        gap = end_time - starting_time
        if gap > 5:
            ending_message = "You took too long to submit. End of typing period. Click reset button to start again"
            sentence.config(fg="yellow", text=ending_message)
            typing_area.config(highlightcolor="red", highlightbackground="red")
            return
        text_len = len(user_line)
        if text_len == len(text_to_display):
            end_of_typing=True

            is_accurate = check_accuracy(user_line, text_to_display)
            seconds_elapsed = end_time-beginning_time
            chars_per_second = round(text_len/seconds_elapsed)
            words_per_minute = chars_per_second * (60/5)
            show_result(is_accurate, words_per_minute)

            all_speeds.append(words_per_minute)
            reset_timer = window.after(2000, reset_app)

    starting_time = time.time()


# function to check user typed sentences is accurate or not
def check_accuracy(user_line, app_line):
    if user_line == app_line:
        return True
    else:
        return False


# function to show result to user
def show_result(boolean, wpm):
    if boolean:
        typing_area.config(highlightcolor="green", highlightbackground="green")
        sentence.config(text=f"speed: {wpm} wpm without errors", fg="green")
    else:
        typing_area.config(highlightbackground="red", highlightcolor="red")
        sentence.config(text=f"speed: {wpm} wpm with errors", fg="red")

# function to reset app and restart all over
def reset_app():
    global end_of_typing, starting_time, user_line, reset_timer,\
        prev_line, text_to_display, beginning_time

    window.after(reset_timer)

    starting_time = 0
    beginning_time = 0
    reset_timer = 0
    end_of_typing = False
    user_line = ""
    prev_line = ""
    text_to_display = assign_sentence(sentences)
    sentence.config(text=text_to_display, fg=FG2)
    typing_area.delete("1.0", "end")
    typing_area.config(highlightcolor=FG, highlightbackground=FG)



# function to show average speed of all sentence user typed
def show_overall_speed():
    global reset_timer

    window.after(reset_timer)

    if len(all_speeds) != 0:
        sum_ = sum(all_speeds)
        avg = sum_/len(all_speeds)

        sentence.config(text=f"{int(avg)} wpm", fg="yellow")
    else:
        sentence.config(text="Nothing to show yet",fg="yellow")

# --------------------UI SETUP----------------------


# variables to hold colors
BG = "#041C32"
FG = "#ECB365"
FG2 = "#FF8F56"
FG3 = "#F3A871"

# variables to hold font family
FONT_FAMILY_1 = "Calibri"
FONT_FAMILY_2 = "Helvetica"

# variables to hold font size
FONT_SIZE_1 = 14
FONT_SIZE_2 = 18
FONT_SIZE_3 = 24

# VARIABLES to hold font styles
FONT_STYLE_1 = "normal"
FONT_STYLE_2 = "italic"

# variables to create font styling
PARA_FONT_1 = (FONT_FAMILY_1, FONT_SIZE_1, FONT_STYLE_1)
PARA_FONT_2 = (FONT_FAMILY_1, 12, FONT_STYLE_2)
HEAD_FONT_1 = (FONT_FAMILY_2, FONT_SIZE_3, FONT_STYLE_2)
HEAD_FONT_2 = (FONT_FAMILY_2, FONT_SIZE_2, FONT_STYLE_1)

# -------------------------------------------------------#

heading_text = "GET YOUR OWN TYPING SPEED TESTED"
text_to_display = assign_sentence(sentences)
instructions = """
1. The test starts the moment you enter your first letter.
2. You can have a pause of only 5 seconds at max.
"""


window.title("Welcome to typing speed calculator")
window.config(bg=BG, padx=50, pady=10)

heading = Label(text=heading_text, font=HEAD_FONT_1, bg=BG, fg=FG, padx=10, pady=10)
heading.grid(row=0, column=0, columnspan=2)

sentence = Label(text=text_to_display,font=HEAD_FONT_2, bg=BG, fg=FG2,pady=10,padx=10,wraplength=800)
sentence.grid(row=1, column=0, columnspan=2)

instruction = Label(text=instructions, font=PARA_FONT_2, bg=BG, fg=FG)
instruction.grid(row=2, column=0, columnspan=2)

typing_area = Text(font=PARA_FONT_1, bg=BG, fg=FG, width=80, height=10, wrap="word", highlightcolor=FG,
                   highlightthickness=4, highlightbackground=FG, padx=5, pady=5)
typing_area.focus()
typing_area.bind("<KeyPress>",start_calculating)
typing_area.grid(row=3, column=0, columnspan=2)

reset_button = Button(text="Reset Application", fg=FG,bg=BG, font=PARA_FONT_1, highlightbackground=FG,
                      highlightthickness=0, highlightcolor=FG,border=3, command=reset_app)
reset_button.grid(row=4, column=0, sticky="ew")

overall_button = Button(text="Show Average speed", fg=FG, bg=BG, font=PARA_FONT_1, highlightbackground=FG,
                        highlightthickness=0, highlightcolor=FG,border=3, command=show_overall_speed)
overall_button.grid(row=4, column=1, sticky="ew")

window.mainloop()

