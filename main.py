import tkinter
from tkinter import RAISED
from tkinter import filedialog as fd

import io
import PIL
from PIL import ImageTk
from PIL import Image

from view import vButton
from agents import encoder

window = tkinter.Tk()

window.title("Cybersecurity - Encode and Transfer")

window.geometry("800x600+10+20")

  # canvas = tkinter.Canvas(window, width=300, height=400)
  # canvas.pack()
  # print(fd)

def UploadAction(event=None):
  file_name = fd.askopenfilename()
  file = ''


  if file_name.endswith('.txt'):
    with open(file_name) as f:
      file = f.read().encode()
  
  if file_name.endswith(('.png', '.jpeg', '.jpg')):
    file = Image.open(file_name).tobytes()
  
 
  encoder.encrypt(file, 'do me')

 
  # print(file_name)


  # img_tkinter = ImageTk.PhotoImage(img)
  
  # label1 = tkinter.Label(image=img_tkinter)
  # label1.image = img_tkinter

  # label1.place(x=200, y=100)


button = tkinter.Button(window, text="Upload", command=UploadAction)
button.pack()

vButton.renderButton(window)

window.mainloop()
