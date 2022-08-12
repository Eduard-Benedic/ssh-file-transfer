"""
=========================================================
Name        :  client.py
Author      :  Eduard Benedic
Description :  SSH client
Sources     :
              {1} - https://docs.paramiko.org/en/stable/api/client.html
              {2} - https://stackoverflow.com/questions/3878082/python-paramiko
=========================================================
"""
from paramiko import SSHClient, AutoAddPolicy
import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)

# create SSHClient {1}, a wrapper arround the Transport, Channel and SFTP client
client = SSHClient()

def send_file(file: bytes, file_extension: str):
  # if the client doesn't recognize the server, initialize the connection anyway {2}
  client.set_missing_host_key_policy(AutoAddPolicy())

  # connect to the server
  client.connect(
    hostname='127.0.0.1',
    port=2200,
    password="foo",
    username="robey"
  )

  sftp = client.open_sftp()

  sftp.putfo(file, file_extension)

  sftp.close()

  client.close()