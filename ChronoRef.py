
import glob
import pathlib
import os
import time
import math
import random
import tkinter.font as font
from tkinter import filedialog
from tkinter import *
from PIL import ImageTk,Image

root = Tk()
root.title('ChronoRef')
#Style
bg_color="#151818"
fg_color="#839699"
accent_color="#094E58"
myFont = font.Font(size=11, family='Arial')
myFont2 = font.Font(size=16, family='Helvetica')
root['bg']=bg_color

#Determines whether or not the next image is random is in sequential order
isRandom=False
#The resize length of the image. If the image is landscape, this effects the width, otherwise the height is affected.
sizemod=900
#The starting time of the timer, 30 seconds.
t=30000
#The index variable for the image list.
n = 0
#The variable for the time that's displayed on the countdown timer.
tc=t

#Asks for directory on application startup
root.directory = filedialog.askdirectory()
dir_path=root.directory

#Creates a list of images in the selected directory
my_images = list(pathlib.Path(dir_path).glob('*.jpg'))
file_count=len(os.listdir(dir_path))

#An image file from the selected directory.
my_img = Image.open(my_images[n])

#Change Directory
def CD():
	global dir_path
	global my_images
	global file_count
	global my_img
	global n
	global my_text_label
	#Selects first image in directory
	n=0
	root.directory = filedialog.askdirectory()
	dir_path=root.directory
	my_images = list(pathlib.Path(dir_path).glob('*.jpg'))
	file_count=len(os.listdir(dir_path))
	my_img = Image.open(my_images[n])
	
	my_label.grid_forget()
	my_text_label.grid_forget()
	updateTime()

#Update countdown time length
def updateTime():
	global tc
	global t
	global my_label
	global my_text_label
	global my_img
	global n
	global h
	global w 
	global ar
	global rw
	global rh
	global tkimage
	global resized 
	global resized_pic
	global my_images
	global sizemod
	t=selected_time.get()
	if tc>0: #manual
		my_label.destroy()
	else: #timer
		my_label.grid_forget()

	tc=t
	imageDisplay()
	

#Update whether the next image is random or sequential
def updateRandom():
	global isRandom

	isRandom=selected_random.get()

#Timer function
def timer():
	global tc

	tc-=1000
	minute = int(math.floor(tc/1000/60))
	second = int(tc/1000%60)
	counter_string = str(minute) +":"+ str(second)

	my_timer.config(text=counter_string)
	my_timer.after(1000, timer)

#Function for loading the next image
def nextImage():
	global my_label
	global my_text_label
	global my_img
	global n
	global h
	global w 
	global ar
	global rw
	global rh
	global tkimage
	global resized 
	global resized_pic
	global my_images
	global tc
	global t
	global isRandom
	global sizemod
	
	#Determines if the timer ran out or the next image was triggered manually by pressing the ">>" button
	if tc>0: #manual
		my_label.destroy()
	else: #timer
		my_label.grid_forget()
	tc=t
	
	#Determines if image selection is random or sequential
	if isRandom:
		n=random.randint(0, len(my_images)-1)
	else:	
		if n<len(my_images)-1:
			n=n+1
		else:
			n=0

	#Wipe grid element, then reload new ones.
	my_text_label.grid_forget()
	
	imageDisplay()
	
#Function for displaying the image
def imageDisplay():
	global my_label
	global my_text_label
	global my_img
	global n
	global h
	global w 
	global ar
	global rw
	global rh
	global tkimage
	global resized 
	global resized_pic
	global my_images
	global tc
	global t
	global isRandom
	global sizemod
	my_img = Image.open(my_images[n])
	tkimage=ImageTk.PhotoImage(my_img)
	
	# Get Image size
	h=tkimage.height()
	w=tkimage.width()
	
	#Determine size of the image. If image length is less than the resize length, it doesn't resize the image.
	ar=h/w
	if ar<1:

		if w>sizemod:
			rw=sizemod
			rh=int(sizemod*ar)


		else:
			rw=w
			rh=h
	else:
		if h>sizemod:
			rh=sizemod
			rw=int(sizemod/ar)
		else:
			rw=w
			rh=h
	root.geometry(str(rw+300)+"x"+str(rh+100))

	resized = my_img.resize((rw,rh), Image.ANTIALIAS)
	resized_pic = ImageTk.PhotoImage(resized)
	
	#Displays the image
	my_label = Label(root, image=resized_pic, bg=bg_color, fg=fg_color, font=myFont)
	my_label.grid(row=2, column=2, rowspan=19)
	
	#Selects the next image after a certain time (t) has passed
	my_label.after(t,nextImage)
	
	#Creates a button that displays the current directory. Clicking it prompts the user to select a new one.
	my_text_label = Button(text=dir_path, bg=bg_color, fg=fg_color, font=myFont, command=CD)
	my_text_label.grid(row=0, column=2)


imageDisplay()


#Adjust the countdown timer length
selected_time=IntVar()
selected_time.set(30000)
r1 = Radiobutton(root, text='30 Seconds', value=30000, variable=selected_time, command=updateTime, bg=bg_color, fg=fg_color, font=myFont, selectcolor=accent_color, indicatoron=0)
r2 = Radiobutton(root, text='1 Minute', value=60000, variable=selected_time, command=updateTime, bg=bg_color, fg=fg_color, font=myFont, selectcolor=accent_color, indicatoron=0)
r3 = Radiobutton(root, text='5 Minutes', value=300000, variable=selected_time, command=updateTime, bg=bg_color, fg=fg_color, font=myFont, selectcolor=accent_color, indicatoron=0)
r4 = Radiobutton(root, text='10 Minutes', value=600000, variable=selected_time, command=updateTime, bg=bg_color, fg=fg_color, font=myFont, selectcolor=accent_color, indicatoron=0)
r5 = Radiobutton(root, text='15 Minutes', value=900000, variable=selected_time, command=updateTime, bg=bg_color, fg=fg_color, font=myFont, selectcolor=accent_color, indicatoron=0)
r6 = Radiobutton(root, text='30 Minutes', value=1800000, variable=selected_time, command=updateTime, bg=bg_color, fg=fg_color, font=myFont, selectcolor=accent_color, indicatoron=0)
r7 = Radiobutton(root, text='45 Minutes', value=2700000, variable=selected_time, command=updateTime, bg=bg_color, fg=fg_color, font=myFont, selectcolor=accent_color, indicatoron=0)
r8 = Radiobutton(root, text='60 Minutes', value=3600000, variable=selected_time, command=updateTime, bg=bg_color, fg=fg_color, font=myFont, selectcolor=accent_color, indicatoron=0)


r1.grid(row=3, column=0, sticky="nsew")
r2.grid(row=4, column=0, sticky="nsew")
r3.grid(row=5, column=0, sticky="nsew")
r4.grid(row=6, column=0, sticky="nsew")
r5.grid(row=7, column=0, sticky="nsew")
r6.grid(row=8, column=0, sticky="nsew")
r7.grid(row=9, column=0, sticky="nsew")
r8.grid(row=10, column=0, sticky="nsew")

#Adjust whether or not the next image is sequential or random
selected_random=BooleanVar()
rl_label = Label(text="Randomize", bg=bg_color, fg=fg_color, font=myFont)
rl_label.grid(row=2, column=3, sticky='w')
rl1 = Radiobutton(root, text='Yes', value=True, variable=selected_random, command=updateRandom, bg=bg_color, fg=fg_color, font=myFont, selectcolor=accent_color, indicatoron=0)
rl2 = Radiobutton(root, text='No', value=False, variable=selected_random, command=updateRandom, bg=bg_color, fg=fg_color, font=myFont, selectcolor=accent_color, indicatoron=0)

rl1.grid(row=3, column=3, sticky='nsew')
rl2.grid(row=4, column=3, sticky='nsew')

#Selects the next image before the timer runs out.
button_right = Button(root, text=">>", command=nextImage, bg=bg_color, fg=fg_color, font=myFont)
button_right.grid(row=0, column=0, pady=10)


#Exit program
button_exit = Button(root, text="X", command=root.quit, bg=bg_color, fg=fg_color, font=myFont)
button_exit.grid(row=0, column=3, sticky="e")


#Displays the timer
my_timer = Label(root, text="", bg=bg_color, fg=fg_color, font=myFont2)
my_timer.grid(row=21,column=1, columnspan=2)

#Starts the timer
timer()


#Allows the window to be draggable
lastClickX = 0
lastClickY = 0


def SaveLastClickPos(event):
    global lastClickX, lastClickY
    lastClickX = event.x
    lastClickY = event.y


def Dragging(event):
    x, y = event.x - lastClickX + root.winfo_x(), event.y - lastClickY + root.winfo_y()
    root.geometry("+%s+%s" % (x , y))


root.overrideredirect(True)
root.attributes('-topmost', True)
root.bind('<Button-1>', SaveLastClickPos)
root.bind('<B1-Motion>', Dragging)

root.resizable(False,False)
root.mainloop()
