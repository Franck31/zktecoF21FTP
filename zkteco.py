import socket
import telnetlib
import sys
from ftplib import FTP
import os

USER = 'root'
HOST = '127.0.0.1'
PASSWORD = 'solokey'
DIRECTORY = 'bad'
LOCALDIR = '/tmp/'


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.settimeout(10)
result = sock.connect_ex((HOST,21))
sock.settimeout(None)
if result == 0:
   ftp = FTP(HOST)
   ftp.login()
   ftp.cwd(DIRECTORY)
   for filename in ftp.nlst():
        localfname = os.path.join(LOCALDIR, filename)
	print 'Getting ' + filename 
        fhandle =  open(localfname, 'wb')
        ftp.retrbinary('RETR ' + filename, fhandle.write)
        fhandle.close()
else:
   tn = telnetlib.Telnet(HOST)
   tn.read_until("login: ")
   tn.write(USER + "\n")
   tn.read_until("Password: ")
   tn.write(PASSWORD + "\n")
   tn.write("nohup tcpsvd -vE 0.0.0.0 21 ftpd  /mnt/mtdblock/data/capture/ & \n")
   tn.write("exit\n")
   print tn.read_all() 
