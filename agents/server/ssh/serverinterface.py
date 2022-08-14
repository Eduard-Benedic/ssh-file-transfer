"""
=========================================================
Name        :  serverinterface.py
Author      :  Eduard Benedic
Description :  implement the server interface.
Sources     :
              {1} - https://docs.paramiko.org/en/stable/api/server.html
=========================================================
"""

from binascii import hexlify
import threading
import paramiko
from paramiko.py3compat import b, u, decodebytes
from paramiko import AUTH_SUCCESSFUL, \
    AUTH_FAILED, OPEN_SUCCEEDED

"""
Class that wraps around the primary thread of paramiko. {1}
"""
class Server(paramiko.ServerInterface):
    # 'data' is the output of base64.b64encode(key)
    # (using the "user_rsa_key" files)
    data = (
        b"AAAAB3NzaC1yc2EAAAABIwAAAIEAyO4it3fHlmGZWJaGrfeHOVY7RWO3P9M7hp"
        b"fAu7jJ2d7eothvfeuoRFtJwhUmZDluRdFyhFY/hFAh76PJKGAusIqIQKlkJxMC"
        b"KDqIexkgHAfID/6mqvmnSJf0b5W8v5h2pI/stOSwTQ+pxVhwJ9ctYDhRSlF0iT"
        b"UWT10hcuO4Ks8="
    )
    good_pub_key = paramiko.RSAKey(data=decodebytes(data))

    def __init__(self):
        self.event = threading.Event()

    def check_channel_request(self, kind, chanid):
        if kind == "session":
            return OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_auth_password(self, username, password):
        if (username == "test") and (password == "test"):
            return paramiko.AUTH_SUCCESSFUL
        return AUTH_FAILED

    def check_auth_publickey(self, username, key):
        print(
            "Auth attempt with key: " + u(
                hexlify(
                    key.get_fingerprint()
                )
            )
        )
        if (username == "test") and (key == self.good_pub_key):
            return AUTH_SUCCESSFUL
        return AUTH_FAILED

    def get_allowed_auths(self, username):
        return "password,publickey"

    def check_channel_shell_request(self, channel):
        self.event.set()
        return True

    def check_channel_pty_request(
        self, channel, term, width, height, pixelwidth, pixelheight, modes
    ):
        return True
