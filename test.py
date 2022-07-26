import pathlib
import time

file_name = 'Ben Howard - Master (with Lyrics).mp3'

def create_file_name(file_name: str):
  path = pathlib.Path(file_name)
  return path.stem + '-' + str(time.time()) + '-' + path.suffix

print(create_file_name(file_name))