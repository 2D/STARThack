import socket
import os

TCP_IP = '169.254.224.107'
TCP_PORT = 1212
buffer_size = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(1)
try:
   s.connect((TCP_IP, TCP_PORT))
   print('success')
   command = '%R1Q,9027:0.52,0.73,0,0,0\r\n'
   print(command)
   s.send(command)
   print(s.recv(4096))
   s.close()
except socket.timeout as e:
   print(e)
