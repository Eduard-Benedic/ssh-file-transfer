"""
=========================================================
Name        :  main.py
Author      :  Eduard Benedic
Description :  GUI rendering
Sources     :
              {1} - https://www.pythontutorial.net/tkinter/tkinter-hello-world/
=========================================================
"""
from ctypes import windll
from tkinter import RAISED
from view import root


# Fix the blur UI on Windows {1}
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
finally:
    root.mainloop()