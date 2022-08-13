from tkinter import filedialog as fd
from agents.client import send_file
from agents.utils import create_file_name
import os
import io

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