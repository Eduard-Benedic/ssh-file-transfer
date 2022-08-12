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
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("", 2200))
except Exception as e:
    print("*** Socket bind failed. Please try another port: " + str(e))
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
        # while True:
            # wait for auth
            # chan = t.accept(20)
            # if chan is None:
            #     print("*** No channel.")
            #     sys.exit(1)
            # print("Authenticated!")

            # server.event.wait(10)
            # if not server.event.is_set():
            #     print("*** Client never asked for a shell.")
            #     sys.exit(1)
            # chan.close()

    except Exception as e:
        print("*** Caught exception: " + str(e.__class__) + ": " + str(e))
        traceback.print_exc()
        try:
            t.close()
        except:
            pass
        sys.exit(1)

while True:
    client, addr = sock.accept()
    try:
        spinServer()
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as exc:
        print

   