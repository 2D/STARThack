import os
import socket
import time
import json
import math

TCP_IP = '169.254.224.107'
TCP_PORT = 1212
buffer_size = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(60)

allData = []

try:
   s.connect((TCP_IP, TCP_PORT))
   print('Connected\n')
   setTargetType = '%R1Q,17021:1\r\n'
   s.send(setTargetType)
   print('Set target type: ' + s.recv(4096))
   for l in range(1,13,1):
      for i in range(30):
         print('l =' + str(l))
         a = (i)*2*math.pi/30
         #b = (l)*math.pi/180
         moveCommand = '%R1Q,9027:' + str(a) + ',' + str(l*0.2) + ',0,0,0\r\n'
         s.send(moveCommand)
         print(str(i) + ' => Move: ' + s.recv(4096))
         angleDistanceCommand = '%R1Q,17017:2\r\n'
         # angleDistanceCommand = '%R1Q,2108:5000,2\r\n'
         datas = None
         for _ in range(3): # Attempt to get angle and distance this many times
            s.send(angleDistanceCommand)
            data = s.recv(4096)
            datas = data.split(',')
            if datas[2] == '0:1285': # Check for error 'only angle measurement vaid'
               print('No valid distance\n')
            else: # Otherwise no more attempts
               break
         datasDict = {}
         datasDict['R1P'] = datas[0]
         datasDict['value0'] = datas[1]
         datasDict['RC'] = datas[2]
         datasDict['angleHorizontal'] = datas[3]
         datasDict['angleVertical'] = datas[4]
         datasDict['lengthSlope'] = datas[5]
         datasDict['modeMeasure'] = datas[6]

         allData.append(datasDict)
         print(len(datas))
         print(datas)
         for j in range(7):
            print(datas[j])
      
   s.close()

   print(allData)
   datas = {}
   datas['datas'] = allData
   #print(json.dumps(allData, indent=4, sort_keys=True))
   with open('data.json','w') as outfile:
      json.dump(datas,outfile)
   #f=open("save.txt","w+")
   #json.dump(allData, indent=4, sort_keys=True)

except socket.timeout as e:
   print(e)
