
import socket
from paramiko import SSHClient, AutoAddPolicy
import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)


def send_file(file: bytes, file_path: str):
  client = SSHClient()

  client.set_missing_host_key_policy(AutoAddPolicy())

  client.connect(hostname='127.0.0.1', port=2200, password="foo", username="robey")
  sftp = client.open_sftp()

  sftp.putfo(file, file_path)

  sftp.close()

  client.close()