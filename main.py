from dst import Dst
import time

d = Dst("")
d.start()
while d.q.qsize() < 10:
	print(d.q.qsize())
	time.sleep(1)
d.q.cont = False

while d.q.qsize() > 0:
	print(d.q.qsize())
	print(d.q.get(timeout=1))

d.t.join()
