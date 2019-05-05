#coding=utf-8
import socket
import binascii
import string
import re
import sys
import os
import time
import struct
import threading

HOST = "0.0.0.0"
PORT = 12345
BUFSIZ = 1024
ADDR = (HOST, PORT)

dataCounter = 0

udpSerSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udpSerSock.bind(ADDR)

bc35TimerFlag = 1#Don't modify this value!
command1 = "AABB01"
command2 = "AABB02"
timerFlag = 0

def bc35Timer():
	global timerFlag
	global docValueData
	global docValueDataFlag
	if bc35TimerFlag == 2:#Don't modify this value
       		# 从flask写入的文件读取数据，通过网络发送给bc35
        	fp = open('/home/ubuntu/python/cache.i','r')
        	docValue = fp.readline()
		docValueData = docValue[0]
		if timerFlag == 0:	
		#第一次给docValueDataFlag赋值，该if下程序只执行一�?
			docValueDataFlag = docValueData
			timerFlag = 1
			print "The frist data of the cache.i file context is : " + docValueData
        		if docValueData == '1':
        			udpSerSock.sendto(command1, addr)
        			print("send data to" + str(addr) + ":" + command1)
	       		elif docValueData == '2':
				udpSerSock.sendto(command2, addr)
        			print("send data to" + str(addr) + ":" + command2)
		if docValueDataFlag != docValueData:#如果数据更新，则执行以下发送程�?
			docValueDataFlag = docValueData#更新为最新数�?
			print "The data of the cache.i file context is : " + docValueData
        		if docValueData == '1':
        			udpSerSock.sendto(command1, addr)
        			print("send data to" + str(addr) + ":" + command1)
	       		elif docValueData == '2':
				udpSerSock.sendto(command2, addr)
        			print("send data to" + str(addr) + ":" + command2)
	timer = threading.Timer(1,bc35Timer)#1s
	timer.start()

while True:
        #print 'Waiting for message from BC35...'
        data, addr = udpSerSock.recvfrom(1024)
        if bc35TimerFlag == 1:
		print "Start timer..."
		bc35TimerFlag = 2#确保获取到地址后Timer启动一�?
		timer = threading.Timer(1,bc35Timer)#1s
		timer.start()
	readstr = str(binascii.b2a_hex(data))   #把接收到的数据转为字符型
        # 接收数据，把数据写入文件，供flask网页读取状�?
	print("receive data from BC35: " + readstr)
        fp = open('/home/ubuntu/python/cache.ii', 'w')
        fp.write(readstr)
        fp.close()

udpSerSock.close()

