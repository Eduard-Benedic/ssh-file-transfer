from tkinter import Button
from tkinter import messagebox


def click():
  messagebox.showinfo("Hello,", "Nice one okay")

def renderButton(window):
  sendBtn = Button(master=window, command=click, text="Submit", bg="blue")
  sendBtn.pack()