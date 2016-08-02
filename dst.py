from scapy.all import *
from Queue import Queue
from threading import Thread
import time

class Dst:
	def __init__(self,ignoreIP):
		self.ignoreIP = ignoreIP
		self.q = Queue()
		self.cont = True

		self.t = Thread(target=self.run)
	
	def __call__(self,packet):
		if IP in packet:
			ip = packet[IP].dst
			if ip != self.ignoreIP:
				self.q.put(ip)
			else:
				print("NOPE!")

	def start(self):
		self.t.start()
		
	
	def run(self):
		while self.cont:
			self.sniff()

	def sniff(self):
		sniff(prn=self,count=1)

if __name__ == "__main__":
	d = Dst("")

	d.start()
	while d.q.qsize() < 10:
		time.sleep(1)
		print(d.q.qsize())
	
	d.cont = False
	d.t.join()
	while d.q.qsize() > 0:
		print(d.q.get())

		
