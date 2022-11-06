import glob
import pathlib
import os
import time
import math
import random
import tkinter.font as font
from tkinter import filedialog
from tkinter import *
from PIL import ImageTk, Image
from natsort import natsorted

root = Tk()
root.title("ChronoRef")
# Style
bg_color = "#151818"
fg_color = "#839699"
accent_color = "#094E58"
my_font = font.Font(size=11, family="Arial")
my_font2 = font.Font(size=16, family="Helvetica")
timer_paused=False

root["bg"] = bg_color

# Determines whether or not the next image is random is in sequential order
is_random = False
# The resize length of the image. If the image is landscape, this effects the width, otherwise the height is affected.
size_mod = 900
# The starting time of the timer, 30 seconds.
timer_count = 30000
# The index variable for the image list.
image_index = 0
# The variable for the time that's displayed on the countdown timer.
timer_display = timer_count

# Asks for directory on application startup
root.directory = filedialog.askdirectory()
dir_path = root.directory

# Creates a list of images in the selected directory
image_list = natsorted(list(pathlib.Path(dir_path).glob("*.jpg")))
file_count = len(os.listdir(dir_path))

# An image file from the selected directory.
image_file = Image.open(image_list[image_index])

# Change Directory
def choose_directory():
    global dir_path
    global image_list
    global file_count
    global image_file
    global image_index
    global directory_label
    global image_frame
    # Selects first image in directory
    image_index = 0
    root.directory = filedialog.askdirectory()
    dir_path = root.directory
    image_list = natsorted(list(pathlib.Path(dir_path).glob("*.jpg")))
    file_count = len(os.listdir(dir_path))
    image_file = Image.open(image_list[image_index])

    display_reset()
    update_time()


def display_reset():
    global image_frame
    global directory_label
    global timer_display
    global timer_count

    if timer_display > 0:  # manual
        image_frame.destroy()
        directory_label.destroy()
    else:  # timer
        image_frame.grid_forget()
        directory_label.grid_forget()

    timer_display = timer_count


# Update countdown time length
def update_time():
    global timer_display
    global timer_count

    timer_count = selected_time.get()

    display_reset()
    image_display()
def resume():
	global timer_display
	global timer_count

	timer_count=timer_display


# Update whether the next image is random or sequential
def updateRandom():
    global is_random
    global button_shuffle

    if is_random == False:
    	button_shuffle = Button(media_control, text="\U0001F500", command=shuffle, bg=bg_color, fg=fg_color, font=my_font2, border=0)
    	button_shuffle.grid(row=0, column=3)

    else:
    	button_shuffle = Button(media_control, text="\U0001F500", command=shuffle, bg=bg_color, fg=accent_color, font=my_font2, border=0)
    	button_shuffle.grid(row=0, column=3)
    	
    display_reset()
    update_time()


def shuffle():
	global is_random

	if is_random == False:
		is_random = True
	else:
		is_random = False
	updateRandom()


# timer function
def timer():
    global timer_display
    global my_timer
    global timer_paused

    if timer_paused==False:

   		timer_display -= 1000
   

    minute = int(math.floor(timer_display / 1000 / 60))
    second = int(timer_display / 1000 % 60)
    counter_string = "{:0>2}".format(str(minute)) + ":" + "{:0>2}".format(str(second))

    my_timer.config(text=counter_string)

    my_timer.after(1000, timer)





def prev_image():
    global image_frame
    global directory_label
    global image_file
    global image_index
    global image_list
    global timer_display
    global timer_count
    global is_random

    # Determines if image selection is random or sequential
    
    if image_index == 0:
        image_index = len(image_list) - 1
    else:
        image_index -= 1

    update_time()

    display_reset()	

    image_display()


# Function for loading the next image
def next_image():
    global image_frame
    global directory_label
    global image_file
    global image_index
    global image_list
    global timer_display
    global timer_count
    global is_random

    # Determines if image selection is random or sequential
    if is_random:
        image_index = random.randint(0, len(image_list) - 1)
    else:
        if image_index < len(image_list) - 1:
            image_index = image_index + 1
        else:
            image_index = 0

    update_time()

    display_reset()	

    image_display()

def pause_timer():
	global timer_paused

	if timer_paused == False:
		timer_paused = True
		resume()

	else:
		timer_paused = False

	display_reset()	

	image_display()	




# Function for displaying the image
def image_display():
    global image_frame
    global directory_label
    global image_file
    global image_index
    global image_height
    global image_width
    global aspect_ratio
    global resize_width
    global resize_height
    global tk_image
    global resized
    global resized_pic
    global image_list
    global timer_display
    global timer_count
    global is_random
    global size_mod
    global timer_paused
    image_file = Image.open(image_list[image_index])
    tk_image = ImageTk.PhotoImage(image_file)

    # Get Image size
    image_height = tk_image.height()
    image_width = tk_image.width()

    # Determine size of the image. If image length is less than the resize length, it doesn't resize the image.
    aspect_ratio = image_height / image_width
    if aspect_ratio < 1:

        if image_width > size_mod:
            resize_width = size_mod
            resize_height = int(size_mod * aspect_ratio)

        else:
            resize_width = image_width
            resize_height = image_height
    else:
        if image_height > size_mod:
            resize_height = size_mod
            resize_width = int(size_mod / aspect_ratio)
        else:
            resize_width = image_width
            resize_height = image_height
    root.geometry(str(resize_width + 300) + "x" + str(resize_height + 100))

    resized = image_file.resize((resize_width, resize_height), Image.ANTIALIAS)
    resized_pic = ImageTk.PhotoImage(resized)

    # Displays the image
    image_frame = Label(root, image=resized_pic, bg=bg_color, fg=fg_color, font=my_font)
    image_frame.grid(row=2, column=2, rowspan=19)

    # Selects the next image after a certain time (timer_count) has passed
    if timer_paused==False:
    	image_frame.after(timer_count, next_image)

    # Creates a button that displays the current directory. Clicking it prompts the user to select a new one.
    directory_label = Button(
        text=dir_path, bg=bg_color, fg=fg_color, font=my_font, command=choose_directory
    )
    directory_label.grid(row=0, column=2)


image_display()


# Adjust the countdown timer length
selected_time = IntVar()
selected_time.set(30000)
r1 = Radiobutton(
    root,
    text="30 Seconds",
    value=30000,
    variable=selected_time,
    command=update_time,
    bg=bg_color,
    fg=fg_color,
    font=my_font,
    selectcolor=accent_color,
    indicatoron=0,
)
r2 = Radiobutton(
    root,
    text="1 Minute",
    value=60000,
    variable=selected_time,
    command=update_time,
    bg=bg_color,
    fg=fg_color,
    font=my_font,
    selectcolor=accent_color,
    indicatoron=0,
)
r3 = Radiobutton(
    root,
    text="5 Minutes",
    value=300000,
    variable=selected_time,
    command=update_time,
    bg=bg_color,
    fg=fg_color,
    font=my_font,
    selectcolor=accent_color,
    indicatoron=0,
)
r4 = Radiobutton(
    root,
    text="10 Minutes",
    value=600000,
    variable=selected_time,
    command=update_time,
    bg=bg_color,
    fg=fg_color,
    font=my_font,
    selectcolor=accent_color,
    indicatoron=0,
)
r5 = Radiobutton(
    root,
    text="15 Minutes",
    value=900000,
    variable=selected_time,
    command=update_time,
    bg=bg_color,
    fg=fg_color,
    font=my_font,
    selectcolor=accent_color,
    indicatoron=0,
)
r6 = Radiobutton(
    root,
    text="30 Minutes",
    value=1800000,
    variable=selected_time,
    command=update_time,
    bg=bg_color,
    fg=fg_color,
    font=my_font,
    selectcolor=accent_color,
    indicatoron=0,
)
r7 = Radiobutton(
    root,
    text="45 Minutes",
    value=2700000,
    variable=selected_time,
    command=update_time,
    bg=bg_color,
    fg=fg_color,
    font=my_font,
    selectcolor=accent_color,
    indicatoron=0,
)
r8 = Radiobutton(
    root,
    text="60 Minutes",
    value=3600000,
    variable=selected_time,
    command=update_time,
    bg=bg_color,
    fg=fg_color,
    font=my_font,
    selectcolor=accent_color,
    indicatoron=0,
)


r1.grid(row=3, column=0, sticky="nsew")
r2.grid(row=4, column=0, sticky="nsew")
r3.grid(row=5, column=0, sticky="nsew")
r4.grid(row=6, column=0, sticky="nsew")
r5.grid(row=7, column=0, sticky="nsew")
r6.grid(row=8, column=0, sticky="nsew")
r7.grid(row=9, column=0, sticky="nsew")
r8.grid(row=10, column=0, sticky="nsew")

# Adjust whether or not the next image is sequential or random
selected_random = BooleanVar()


# Media Control Frame

media_control = Frame(root)
media_control.grid(row=22, column=2)

# Media Control Buttons


button_shuffle = Button(
    media_control, text="\U0001F500", command=shuffle, bg=bg_color, fg=fg_color, font=my_font2, border=0

)
button_shuffle.grid(row=0, column=3)

button_right = Button(
    media_control, text="\u23ED", command=next_image, bg=bg_color, fg=fg_color, font=my_font2, border=0
)
button_right.grid(row=0, column=2)

button_pause = Button(
    media_control, text="\u23EF", command=pause_timer, bg=bg_color, fg=fg_color, font=my_font2, border=0

)
button_pause.grid(row=0, column=1)

button_left = Button(
    media_control, text="\u23EE", command=prev_image, bg=bg_color, fg=fg_color, font=my_font2, border=0

)
button_left.grid(row=0, column=0)

# Exit program
button_exit = Button(
    root, text="\u2715", command=root.quit, bg=bg_color, fg=fg_color, font=my_font
)
button_exit.grid(row=0, column=3, sticky="e")


# Displays the timer
my_timer = Label(root, text="", bg=bg_color, fg=fg_color, font=my_font2)
my_timer.grid(row=21, column=1, columnspan=2)

# Starts the timer
timer()


# Allows the window to be draggable
lastClickX = 0
lastClickY = 0


def SaveLastClickPos(event):
    global lastClickX, lastClickY
    lastClickX = event.x
    lastClickY = event.y


def Dragging(event):
    x, y = event.x - lastClickX + root.winfo_x(), event.y - lastClickY + root.winfo_y()
    root.geometry("+%s+%s" % (x, y))


root.overrideredirect(True)
root.attributes("-topmost", True)
root.bind("<Button-1>", SaveLastClickPos)
root.bind("<B1-Motion>", Dragging)

root.resizable(False, False)
root.mainloop()
