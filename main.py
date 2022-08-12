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


def create_file_name(file_name: str):
  path = pathlib.Path(file_name)
  return path.stem + '-' + str(time.time()) + path.suffix

def UploadAction(event=None):
  full_path = fd.askopenfilename()
  file = ''
  file_name = os.path.split(full_path)[-1]


  if full_path.endswith('.txt'):
    with open(full_path, 'r') as f:
      send_file(f, create_file_name(file_name))

  elif full_path.endswith(('.png', '.jpeg', '.jpg', '.JPG', '.mp3', '.mp4', '.pdf')):
    with open(full_path,'rb') as bytes:
      send_file(bytes, create_file_name(file_name))


button = tkinter.Button(window, text="Upload", command=UploadAction)
button.pack()

vButton.renderButton(window)

window.mainloop()
