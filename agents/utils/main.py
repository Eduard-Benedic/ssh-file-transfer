"""
=========================================================
Name        :  main.py
Author      :  Eduard Benedic
Description :  util functions
Sources     :
=========================================================
"""

import time
import pathlib

def create_file_name(file_name: str):
  path = pathlib.Path(file_name)
  return path.stem + '-' + str(time.time()) + path.suffix