import tkinter
from tkinter import RAISED
import os
import io
import time
import pathlib
from tkinter import filedialog as fd
from PIL import ImageTk
from PIL import Image

from view import vButton
from agents import encoder, send_file

window = tkinter.Tk()

window.title("Cybersecurity - Encode and Transfer")

window.geometry("1200x800+10+20")

  # canvas = tkinter.Canvas(window, width=300, height=400)
  # canvas.pack()
  # print(fd)


def create_file_name(file_name: str):
  path = pathlib.Path(file_name)
  return path.stem + '-' + str(time.time()) + path.suffix

def UploadAction(event=None):
  full_path = fd.askopenfilename()
  file = ''
  file_name = os.path.split(full_path)[-1]

  if full_path.endswith('.txt'):
    with open(full_path, 'r') as f:
      send_file(f,'files/' +  create_file_name(file_name))
  
  if full_path.endswith(('.png', '.jpeg', '.jpg', '.JPG')):
    # print(img.format)
    with open(full_path,'rb') as img:
      send_file(img,'files/' +  create_file_name(file_name))

  if full_path.endswith(('.mp3', '.mp4')):
     with open(full_path,'rb') as audio:
      send_file(audio, 'files/' + create_file_name(file_name))
  
  # encoder.encrypt(file, 'do me')

  

 
  # print(file_name)


  # img_tkinter = ImageTk.PhotoImage(img)
  
  # label1 = tkinter.Label(image=img_tkinter)
  # label1.image = img_tkinter

  # label1.place(x=200, y=100)


button = tkinter.Button(window, text="Upload", command=UploadAction)
button.pack()

vButton.renderButton(window)

window.mainloop()
