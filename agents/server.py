#!/usr/bin/env python

# Copyright (C) 2003-2007  Robey Pointer <robeypointer@gmail.com>
#
# This file is part of paramiko.
#
# Paramiko is free software; you can redistribute it and/or modify it under the
# terms of the GNU Lesser General Public License as published by the Free
# Software Foundation; either version 2.1 of the License, or (at your option)
# any later version.
#
# Paramiko is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Paramiko; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301 USA.

import base64
from binascii import hexlify
import os
import socket
import sys
import threading
import traceback
import signal
import paramiko
from paramiko.py3compat import b, u, decodebytes
import os
from paramiko import ServerInterface, SFTPServerInterface, SFTPServer, SFTPAttributes, \
    SFTPHandle, SFTP_OK, AUTH_SUCCESSFUL, OPEN_SUCCEEDED



signal.signal(signal.SIGINT, signal.SIG_DFL)
# setup logging
paramiko.util.log_to_file("demo_server.log")

host_key = paramiko.RSAKey(filename="keys/server")
# host_key = paramiko.DSSKey(filename='test_dss.key')

print("Read key: " + u(hexlify(host_key.get_fingerprint())))


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
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_auth_password(self, username, password):
        if (username == "robey") and (password == "foo"):
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED

    def check_auth_publickey(self, username, key):
        print("Auth attempt with key: " + u(hexlify(key.get_fingerprint())))
        if (username == "robey") and (key == self.good_pub_key):
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED

    # def check_auth_gssapi_with_mic(
    #     self, username, gss_authenticated=paramiko.AUTH_FAILED, cc_file=None
    # ):
    #     """
    #     .. note::
    #         We are just checking in `AuthHandler` that the given user is a
    #         valid krb5 principal! We don't check if the krb5 principal is
    #         allowed to log in on the server, because there is no way to do that
    #         in python. So if you develop your own SSH server with paramiko for
    #         a certain platform like Linux, you should call ``krb5_kuserok()`` in
    #         your local kerberos library to make sure that the krb5_principal
    #         has an account on the server and is allowed to log in as a user.
    #     .. seealso::
    #         `krb5_kuserok() man page
    #         <http://www.unix.com/man-page/all/3/krb5_kuserok/>`_
    #     """
    #     if gss_authenticated == paramiko.AUTH_SUCCESSFUL:
    #         return paramiko.AUTH_SUCCESSFUL
    #     return paramiko.AUTH_FAILED

    # def check_auth_gssapi_keyex(
    #     self, username, gss_authenticated=paramiko.AUTH_FAILED, cc_file=None
    # ):
    #     if gss_authenticated == paramiko.AUTH_SUCCESSFUL:
    #         return paramiko.AUTH_SUCCESSFUL
    #     return paramiko.AUTH_FAILED

    # def enable_auth_gssapi(self):
    #     return True

    def get_allowed_auths(self, username):
        # return "gssapi-keyex,gssapi-with-mic,password,publickey"
        return "password,publickey"

    def check_channel_shell_request(self, channel):
        self.event.set()
        return True

    def check_channel_pty_request(
        self, channel, term, width, height, pixelwidth, pixelheight, modes
    ):
        return True


DoGSSAPIKeyExchange = True

# now connect
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("", 2200))
except Exception as e:
    print("*** Bind failed: " + str(e))
    traceback.print_exc()
    sys.exit(1)

try:
    sock.listen(100)
    print("Listening for connection ...")
    client, addr = sock.accept()
except Exception as e:
    print("*** Listen/accept failed: " + str(e))
    traceback.print_exc()
    sys.exit(1)

print("Got a connection!")


class StubSFTPHandle (SFTPHandle):
    def stat(self):
        try:
            return SFTPAttributes.from_stat(os.fstat(self.readfile.fileno()))
        except OSError as e:
            return SFTPServer.convert_errno(e.errno)

    def chattr(self, attr):
        # python doesn't have equivalents to fchown or fchmod, so we have to
        # use the stored filename
        try:
            SFTPServer.set_file_attr(self.filename, attr)
            return SFTP_OK
        except OSError as e:
            return SFTPServer.convert_errno(e.errno)


class StubSFTPServer (SFTPServerInterface):
    # assume current folder is a fine root
    # (the tests always create and eventualy delete a subfolder, so there shouldn't be any mess)
    ROOT = os.getcwd()
        
    def _realpath(self, path):
        return self.ROOT + self.canonicalize(path)

    def list_folder(self, path):
        path = self._realpath(path)
        try:
            out = [ ]
            flist = os.listdir(path)
            for fname in flist:
                attr = SFTPAttributes.from_stat(os.stat(os.path.join(path, fname)))
                attr.filename = fname
                out.append(attr)
            return out
        except OSError as e:
            return SFTPServer.convert_errno(e.errno)

    def stat(self, path):
        path = self._realpath(path)
        try:
            return SFTPAttributes.from_stat(os.stat(path))
        except OSError as e:
            return SFTPServer.convert_errno(e.errno)

    def lstat(self, path):
        path = self._realpath(path)
        try:
            return SFTPAttributes.from_stat(os.lstat(path))
        except OSError as e:
            return SFTPServer.convert_errno(e.errno)

    def open(self, path, flags, attr):
        path = self._realpath(path)
        try:
            binary_flag = getattr(os, 'O_BINARY',  0)
            flags |= binary_flag
            mode = getattr(attr, 'st_mode', None)
            if mode is not None:
                fd = os.open(path, flags, mode)
            else:
                # os.open() defaults to 0777 which is
                # an odd default mode for files
                fd = os.open(path, flags, 0o666)
        except OSError as e:
            return SFTPServer.convert_errno(e.errno)
        if (flags & os.O_CREAT) and (attr is not None):
            attr._flags &= ~attr.FLAG_PERMISSIONS
            SFTPServer.set_file_attr(path, attr)
        if flags & os.O_WRONLY:
            if flags & os.O_APPEND:
                fstr = 'ab'
            else:
                fstr = 'wb'
        elif flags & os.O_RDWR:
            if flags & os.O_APPEND:
                fstr = 'a+b'
            else:
                fstr = 'r+b'
        else:
            # O_RDONLY (== 0)
            fstr = 'rb'
        try:
            f = os.fdopen(fd, fstr)
        except OSError as e:
            return SFTPServer.convert_errno(e.errno)
        fobj = StubSFTPHandle(flags)
        fobj.filename = path
        fobj.readfile = f
        fobj.writefile = f
        return fobj

    def remove(self, path):
        path = self._realpath(path)
        try:
            os.remove(path)
        except OSError as e:
            return SFTPServer.convert_errno(e.errno)
        return SFTP_OK

    def rename(self, oldpath, newpath):
        oldpath = self._realpath(oldpath)
        newpath = self._realpath(newpath)
        try:
            os.rename(oldpath, newpath)
        except OSError as e:
            return SFTPServer.convert_errno(e.errno)
        return SFTP_OK

    def mkdir(self, path, attr):
        path = self._realpath(path)
        try:
            os.mkdir(path)
            if attr is not None:
                SFTPServer.set_file_attr(path, attr)
        except OSError as e:
            return SFTPServer.convert_errno(e.errno)
        return SFTP_OK

    def rmdir(self, path):
        path = self._realpath(path)
        try:
            os.rmdir(path)
        except OSError as e:
            return SFTPServer.convert_errno(e.errno)
        return SFTP_OK

    def chattr(self, path, attr):
        path = self._realpath(path)
        try:
            SFTPServer.set_file_attr(path, attr)
        except OSError as e:
            return SFTPServer.convert_errno(e.errno)
        return SFTP_OK

    def symlink(self, target_path, path):
        path = self._realpath(path)
        if (len(target_path) > 0) and (target_path[0] == '/'):
            # absolute symlink
            target_path = os.path.join(self.ROOT, target_path[1:])
            if target_path[:2] == '//':
                # bug in os.path.join
                target_path = target_path[1:]
        else:
            # compute relative to path
            abspath = os.path.join(os.path.dirname(path), target_path)
            if abspath[:len(self.ROOT)] != self.ROOT:
                # this symlink isn't going to work anyway -- just break it immediately
                target_path = '<error>'
        try:
            os.symlink(target_path, path)
        except OSError as e:
            return SFTPServer.convert_errno(e.errno)
        return SFTP_OK

    def readlink(self, path):
        path = self._realpath(path)
        try:
            symlink = os.readlink(path)
        except OSError as e:
            return SFTPServer.convert_errno(e.errno)
        # if it's absolute, remove the root
        if os.path.isabs(symlink):
            if symlink[:len(self.ROOT)] == self.ROOT:
                symlink = symlink[len(self.ROOT):]
                if (len(symlink) == 0) or (symlink[0] != '/'):
                    symlink = '/' + symlink
            else:
                symlink = '<error>'
        return symlink

try:
    # t = paramiko.Transport(client, gss_kex=DoGSSAPIKeyExchange)
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

    # wait for auth
    chan = t.accept(20)
    if chan is None:
        print("*** No channel.")
        sys.exit(1)
    print("Authenticated!")

    server.event.wait(10)
    if not server.event.is_set():
        print("*** Client never asked for a shell.")
        sys.exit(1)

    # chan.send("\r\n\r\nWelcome to my dorky little BBS!\r\n\r\n")
    # chan.send(
    #     "We are on fire all the time!  Hooray!  Candy corn for everyone!\r\n"
    # )
    # chan.send("Happy birthday to Robot Dave!\r\n\r\n")
    # chan.send("Username: ")
    
    # print(chan.recv(1024))

    # t.set_subsystem_handler('sftp', paramiko.SFTPServer, StubSFTPServer)
  
    # f = chan.makefile("rU")
    # username = f.readline().strip("\r\n")
    # chan.send("\r\nI don't like you, " + username + ".\r\n")
    chan.close()

except Exception as e:
    print("*** Caught exception: " + str(e.__class__) + ": " + str(e))
    traceback.print_exc()
    try:
        t.close()
    except:
        pass
    sys.exit(1)


# import os
# import signal
# import socket
# import sys
# import traceback
# import paramiko
# from paramiko import Transport

# signal.signal(signal.SIGINT, signal.SIG_DFL)
# host_key = paramiko.RSAKey(filename="keys/server")

# class Server(paramiko.ServerInterface):  
#   def check_channel_request(self, kind, chanid):
#     if kind == "session":
#       return paramiko.OPEN_SUCCEDED

#   def check_auth_publickey(self, username, key):
#     return paramiko.AUTH_SUCCESSFUL

#   def get_allowed_auth(self, username):
#     return "password, publickey"
  
#   def check_auth_none(self, username):
#     return paramiko.AUTH_SUCCESSFUL

#   def check_auth_password(self, username, password):
#     return paramiko.AUTH_SUCCESSFUL


# try:
#   sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#   sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#   sock.bind(("127.0.0.1", 8800))
# except Exception as e:
#   print("*** Bind failed: " + str(e))
#   traceback.print_exc()

# print("Connection establised")

# try:
#   sock.listen(100)
#   print("Waiting for a connection")
#   client, addr = sock.accept()
#   print(client, addr)
#   print("I think someone connected")
# except Exception as e:
#   print("Listen/accept has failed" + str(e))
#   traceback.print_exc()
#   sys.exit(1)

# try:
#   transport = paramiko.Transport(client)
#   transport.set_gss_host(socket.getfqdn(""))
#   try:
#     transport.load_server_moduli()
#   except:
#     print("Failed to load moduli -- gex will be unsupported")
#     raise

#   transport.add_server_key(host_key)
#   server = Server()

#   try:
#     transport.start_server(server=server)
#   except paramiko.SSHException:
#     print("SSH negotiation failed.")
#     sys.exit(1)
#   chan = transport.accept(20)

#   print(chan.recv())
#   if chan is None:
#     print("*** No channel.")
#     sys.exit(1)
#   print("Authenticated!")

# except Exception as e:
#   print("Caught expression: " + str(e.__class__) + " : " + str(e))
#   traceback.print_exc()
#   try:
#     transport.close()
#   except:
#     pass
#   sys.exit(1)

  