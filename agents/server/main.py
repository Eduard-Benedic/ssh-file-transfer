"""
=========================================================
Name        :  main.py
Author      :  Eduard Benedic
Description :  package that encapsulates the ssh implementation and spins up a server on top of the
               TCP/IP protocol. It has the main role of opening a socket and creating the SSH connection
               on top of it.
Sources     :
              {1} - https://docs.python.org/3/howto/sockets.html
              {2} - https://pythontic.com/modules/socket/accept
=========================================================
"""

from binascii import hexlify
import socket
import sys
import threading
import traceback
import signal
import paramiko
from paramiko.py3compat import b, u, decodebytes
import os
from ssh import StubSFTPServer, StubSFTPHandle
from ssh import Server


signal.signal(signal.SIGINT, signal.SIG_DFL)
# setup logging
paramiko.util.log_to_file("demo_server.log")

host_key = paramiko.RSAKey(filename="keys/server")

print("Read key: " + u(hexlify(host_key.get_fingerprint())))


try:
    # open a socket and set the protocol to TCP/IP {1}
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("", 2200))
except Exception as e:
    print("*** Socket bind failed. Choose another port: " + str(e))
    traceback.print_exc()
    sys.exit(1)

sock.listen(100)
print("Listening for connection ...")

def spinServer():
    try:
        t = paramiko.Transport(client)
        t.set_gss_host(socket.getfqdn(""))
        try:
            t.load_server_moduli()
        except:
            print("(Failed to load moduli -- gex will be unsupported.)")
            raise
        t.add_server_key(host_key)
        t.set_subsystem_handler('sftp', paramiko.SFTPServer, StubSFTPServer)
        server = Server()

        try:
            t.start_server(server=server)
        except paramiko.SSHException:
            print("*** SSH negotiation failed.")
            sys.exit(1)

    except Exception as e:
        print("*** Caught exception: " + str(e.__class__) + ": " + str(e))
        traceback.print_exc()
        try:
            t.close()
        except:
            pass
        sys.exit(1)

while True:
    # accept connections on the initialized socket {2}
    client, addr = sock.accept()
    try:
        spinServer()
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as exc:
        print

   