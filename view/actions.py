"""
=========================================================
Name        :  client.py
Author      :  Eduard Benedic
Description :  contains the actions that will be attached to the button
Sources     :
              {1} - https://www.geeksforgeeks.org/understanding-file-sizes-bytes-kb-mb-gb-tb-pb-eb-zb-yb/
=========================================================
"""
from tkinter import filedialog as fd
from agents.client import send_file
from agents.utils import create_file_name
import os
import time


def uploadAction(event=None):
  full_path = fd.askopenfilename()
  file = ''
  file_name = os.path.split(full_path)[-1]
  
  start = time.time()
  if full_path.endswith('.txt'):
    with open(full_path, 'r') as f:
      send_file(f, '/files/'+ create_file_name(file_name))

  elif full_path.endswith(
    ('.png', '.jpeg', '.jpg', '.JPG', '.mp3', '.mp4', '.pdf')
  ):
    with open(full_path,'rb') as bytes:
      send_file(bytes, '/files/' +  create_file_name(file_name))

  end = time.time()
  print("Time elapsed in msec:{}".format((end - start) * 1000))