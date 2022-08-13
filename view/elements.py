import tkinter
from tkinter import Button
from tkinter import filedialog as fd

from .actions import uploadAction

primary = '#00594c'
textPrimary = '#fff'
light = '#068b78'

buttonStyles = {
  'bg': primary,
  'activebackground': light,
  'fg': textPrimary,
  'bd': 0,
  'font': '200',
  'height': 2,
  'width': 6,
  'padx': 20
}

class Artist:
  def __init__(self, root):
    self.root = root
    self._configure_window()

  def draw_title(self, text):
    title = tkinter.Label(
      self.root,
      text=text,
      font=200,
      pady=50
    )
    title.pack()

  def draw_button(self, text, command):
    uploadButton = Button(master=self.root, text=text, command=command, **buttonStyles)
    uploadButton.pack()

  def _configure_window(self):
    screen_width = self.root.winfo_screenwidth()
    screen_height = self.root.winfo_screenheight()

    self.root.title("File transfer over secure connection")
    self.root.geometry(f'{screen_width}x{screen_height}+0+0')
    self.root.resizable(True, True)


root = tkinter.Tk()

artist = Artist(root)
artist.draw_button('Upload', uploadAction)
artist.draw_title('File transfer over secure SSH connection')
