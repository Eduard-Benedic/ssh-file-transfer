from cgitb import text
from tkinter import Button
from tkinter import messagebox
from tkinter import filedialog as fd
import os
import io

from agents.client import send_file
from agents.utils import create_file_name

primary = '#00594c'
textPrimary = '#fff'
light = '#068b78'

buttonStyles = {
  'bg': primary,
  'activebackground': light,
  'fg': textPrimary,
  'bd': 0,
  'font': '4000px',
  'height': 2,
  'width': 6,
  'padx': 20
}


def click():
  messagebox.showinfo("Hello,", "Nice one okay")

def uploadAction(event=None):
  full_path = fd.askopenfilename()
  file = ''
  file_name = os.path.split(full_path)[-1]

  if full_path.endswith('.txt'):
    with open(full_path, 'r') as f:
      send_file(f, create_file_name(file_name))

  elif full_path.endswith(('.png', '.jpeg', '.jpg', '.JPG', '.mp3', '.mp4', '.pdf')):
    with open(full_path,'rb') as bytes:
      send_file(bytes, create_file_name(file_name))

def renderButton(window):
  sendBtn = Button(
    master=window,
    text="Submit",
    command=click,
    **buttonStyles
  )
  uploadButton = Button(master=window, text="Upload", command=uploadAction, **buttonStyles)

  sendBtn.pack()
  uploadButton.pack()
