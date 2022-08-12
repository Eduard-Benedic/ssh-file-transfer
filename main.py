import tkinter
from tkinter import RAISED


# Import gui elements elements
from view import vButton

window = tkinter.Tk()

window.title("Cybersecurity - Encode and Transfer")

window.geometry("1200x800+10+20")

vButton.renderButton(window)

window.mainloop()
