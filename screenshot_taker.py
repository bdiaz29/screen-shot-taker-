from mss import mss
from tkinter import *
from PIL import Image, ImageDraw
import numpy as np
import cv2
import time
import datetime
import random
from PIL import ImageTk

destination = ''
# screen_pic=None
window = Tk()
window.title("screen shot application")
window.geometry('300x300')
file_frame = Frame(master=window)
file_frame.grid(column=0, row=0)
from tkinter import filedialog

sct = mss()

#assign initial values to coordinates
x1 = 0
y1 = 0
x2 = 224
y2 = 224


# pop up to select area of screen to copy
def popup():
    global screen_pic

    # draws a rectangle when selecting the area
    def motion(event):
        # imports the full screen screen shot 
        # and the coordinates when first clicked 
        global x1, x2, screen_pic
        x = int(event.x)
        y = int(event.y)
        # asssigns the appropriate values to draw the rectangle
        xmin = min(x1, x)
        xmax = max(x1, x)
        ymin = min(y1, y)
        ymax = max(y1, y)
        # represents the top left corner of rectangle
        start_point = (xmin, ymin)
        # represents the bottom right corner of rectangle
        end_point = (xmax, ymax)
        # Blue color in BGR
        color = (255, 0, 0)
        # Line thickness of 2 px
        thickness = 2
        # Draw a rectangle with blue line borders of thickness of 2 px
        temp = np.array(screen_pic)
        image = cv2.rectangle(temp, start_point, end_point, color, thickness)
        img4 = Image.fromarray(np.uint8(np.array(image)))
        # test=Image.fromarray(np.uint8(np.ones((224,224,3))))
        tk_img = ImageTk.PhotoImage(img4)
        picture_lbl.configure(image=tk_img)
        picture_lbl.image = tk_img

    # assign the coordinates when mouse first clicked
    def mouse_click(event):
        global x1, y1
        x1 = event.x
        y1 = event.y

    # assign the coordinates when mouse is released
    def mouse_release(event):
        global x2, y2, x1, y1
        x2 = int(event.x)
        y2 = int(event.y)

        xmin = min(x1, x2)
        xmax = max(x1, x2)
        ymin = min(y1, y2)
        ymax = max(y1, y2)

        top_ = str(ymin * 2)
        left = str(xmin * 2)
        bottom = str(ymax * 2)
        right = str(xmax * 2)
        # changes values in entry box
        top_txt.delete(0, "end")
        left_txt.delete(0, "end")
        bottom_txt.delete(0, "end")
        right_txt.delete(0, "end")

        top_txt.insert(END, str(top_))
        left_txt.insert(END, str(left))
        bottom_txt.insert(END, str(bottom))
        right_txt.insert(END, str(right))

        top.destroy()

    # takes screen shot of full monitor
    with mss() as sct:
        mon = sct.monitors[0]
        box = {
            'top': mon['top'],
            'left': mon['left'],
            'width': mon['width'],
            'height': mon['height'],
        }
        sct_img = sct.grab(box)
        sct_img = np.array(sct_img)
        sct_img = sct_img[:, :, [2, 1, 0]]
    # resize the full sized image to half
    s = np.shape(sct_img)
    height = s[0]
    width = s[1]
    h = int(height / 2)
    w = int(width / 2)
    new_img = cv2.resize(sct_img, (w, h))
    # removed 4th dimension
    screen_pic = new_img[:, :, 0:3]

    top = Toplevel()
    top.title("About this application...")
    # msg = Message(top, text="copy area")
    # msg.grid(column=0, row=0)
    # button = Button(top, text="Dismiss", command=top.destroy)
    # button.grid(column=1, row=0)
    img4 = Image.fromarray(np.uint8(np.array(new_img)))
    # test=Image.fromarray(np.uint8(np.ones((224,224,3))))
    tk_img = ImageTk.PhotoImage(img4)
    picture_lbl = Label(top, image=tk_img, cursor='crosshair')
    picture_lbl.image = tk_img
    picture_lbl.grid(column=2, row=0)

    picture_lbl.bind("<ButtonRelease-1>", mouse_release)
    picture_lbl.bind("<B1-Motion>", motion)
    picture_lbl.bind("<ButtonPress-1>", mouse_click)


# saves the directory to save the screenshots
def save_dir():
    global destination
    dest_String = filedialog.askdirectory(initialdir="E:/machine learning")
    destination = dest_String + '/'
    start_btn.configure(state='normal')


def take_screenshot():
    global destination
    print("screenshot")
    top = int(top_txt.get())
    left = int(left_txt.get())

    bottom = int(bottom_txt.get())
    right = int(right_txt.get())

    height = bottom - top
    width = right - left
    with mss() as sct:
        # initiate the grab monitor
        monitor = {"top": top, "left": left, "width": width, "height": height}
        sct_img = sct.grab(monitor)
        sct_img = np.array(sct_img)
        # read in array channels backward to convert to rgb
        # img=sct_img
        img = sct_img[:, :, [2, 1, 0]]
        img = np.uint8(img)
        # takes the current date time
        datetime_object = str(datetime.datetime.now())
        # replace all the parts of the string to allow it to be saved 
        # as a file
        A = datetime_object.replace('.', '')
        B = A.replace('-', '')
        C = B.replace(':', '')
        print(str(datetime_object))
        image = Image.fromarray(img)
        image.save(destination + C + '.jpeg')


dir_btn = Button(master=file_frame, text="specify save directory", command=save_dir)
dir_btn.grid(column=0, row=0, padx=5, pady=5)

load_h5_lbl = Label(master=file_frame)
load_h5_lbl.grid(column=1, row=0, padx=5, pady=5)

top_lbl = Label(master=file_frame, text="Top position")
top_lbl.grid(column=0, row=1, padx=5, pady=5)

left_lbl = Label(master=file_frame, text="Left position")
left_lbl.grid(column=0, row=2, padx=5, pady=5)

width_lbl = Label(master=file_frame, text="capture screen size")
width_lbl.grid(column=0, row=3, padx=5, pady=5)

top_txt = Entry(master=file_frame)
top_txt.grid(column=1, row=1, padx=5, pady=5)
top_txt.insert(END, "0")

left_txt = Entry(master=file_frame)
left_txt.grid(column=1, row=2, padx=5, pady=5)
left_txt.insert(END, "0")

bottom_txt = Entry(master=file_frame)
bottom_txt.grid(column=1, row=3, padx=5, pady=5)
bottom_txt.insert(END, "224")

right_txt = Entry(master=file_frame)
right_txt.grid(column=1, row=4, padx=5, pady=5)
right_txt.insert(END, "224")

start_btn = Button(master=file_frame, text="take screen shot", command=take_screenshot)
start_btn.grid(column=0, row=5, padx=5, pady=5)
start_btn.configure(state='disabled')

copy_btn = Button(master=file_frame, text="copy area ", command=popup)
copy_btn.grid(column=0, row=6, padx=5, pady=5)
copy_btn.configure(state='normal')

window.mainloop()
