from scapy.all import *
from Queue import Queue
import time
import random
import sys

class Recorder:
	def __init__(self,ignoreIP):
		self.ignoreIP = ignoreIP
		self.q = Queue()
	
	def __call__(self,packet):
		if IP in packet:
			ip = packet[IP].dst
			if ip not in self.ignoreIP:
				self.q.put(packet)
			else:
				pass

	def packetString(self,packet):
		'''
		Current format:
		time,dst,src
		'''
		ret = str(packet.time) + ','
		ret += str(packet[IP].dst) + ','
		ret += str(packet[IP].src) + '\n'
		return ret
	
	def getPString(self):
		return self.packetString(self.q.get())

	def sniff(self,count=1):
		sniff(prn=self,count=count)

if __name__ == "__main__":
	f = open("addresses.csv","a")
	r = Recorder(["192.168.0.10","127.0.0.1","239.255.255.250"])
	while 1:
		r.sniff(count=10)
		while r.q.qsize() > 0:
			f.write(r.getPString())
			f.flush()
