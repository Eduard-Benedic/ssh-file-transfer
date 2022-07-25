
import socket
from paramiko import SSHClient
import signal
import paramiko
from base64 import decodebytes
signal.signal(signal.SIGINT, signal.SIG_DFL)

client = SSHClient()

client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# client.load_host_keys(filename="keys/client")
# client.set_missing_host_key_policy(paramiko.WarningPolicy())

client.connect(hostname='127.0.0.1', port=2200, password="foo", username="robey")

# chan = client.invoke_shell()
# print(chan.recv(3000))

# text = str("Hello server. Kindly accept my request.").encode("utf")
# chan.send(bytes(text))

sftp = client.open_sftp()

sftp.put("send.txt", "files/whatever.txt")
sftp.close()
client.close()