from scapy.all import *
from Queue import Queue
from threading import Thread
import time
import sqlite3
import random
import sys

class Dst:
	def __init__(self,ignoreIP):
		self.ignoreIP = ignoreIP
		self.q = Queue()
		self.cont = True

		self.t = Thread(target=self.run)
	
	def __call__(self,packet):
		if IP in packet:
			ip = packet[IP].dst
			if ip not in self.ignoreIP:
				self.q.put(ip)
			else:
				pass
#				print("NOPE!")

	def start(self):
		self.t.start()
		
	
	def run(self):
		while self.cont:
#			print(self.cont)
			self.sniff()

	def sniff(self):
		sniff(prn=self,count=1)

if __name__ == "__main__":
	d = Dst(["192.168.0.10","127.0.0.1"])
#	f = open("addresses.csv","a")
	dbc = sqlite3.connect("ipmap.db")
	c = dbc.cursor()
	while 1:
		with open("cont",'r') as cont:
			val = cont.read()
			if int(val) == 0:
				break
			#print("cont: ",val)
		while d.q.qsize() < 1:
			d.sniff()
		addr = d.q.get()
		print(addr)
#		f.write(str(addr))
#		f.write("\n")
#		f.flush()
		written = False
		trycount = 0
		while not written and trycount < 10:
			try:
				c.execute("INSERT INTO dest VALUES('{0}');".format(addr))
				written = True
			except Exception as e:
				time.sleep(random.random()*2)
				trycount += 1
				print("try count at {0}".format(trycount),e)
		dbc.commit()
	
	print("dst has shutdown.")
	sys.exit(0)
