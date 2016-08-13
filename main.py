import time
from subprocess import Popen
import sqlite3
import sys

conn = sqlite3.connect("ipmap.db")
c = conn.cursor()

c.execute("CREATE TABLE IF NOT EXISTS dest(addr TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS route(addr TEXT, count INT)")
c.execute("CREATE TABLE IF NOT EXISTS step(dest TEXT, step TEXT, step_num INT)")
c.execute("CREATE TABLE IF NOT EXISTS geoloc(addr TEXT, lat REAL, lon REAL)")



with open("cont","w") as f:
	f.write("1")

addr = Popen(['python','dst.py'])

c.execute("SELECT * FROM dest WHERE addr NOT IN (SELECT addr FROM route)")

new_routes = c.fetchall()

try:
	time.sleep(5)
except:
	pass

with open("cont","w") as f:
	f.write("0")

children = True
while children:
	ccount = 0
	children = False
	addr.poll()
	if addr.returncode == None:
		children = True
		sys.stdout.write('dst is still running.{0}   \r'.format(time.time()))
	else:
		sys.stdout.write('dst has stoped.      {0}   \r'.format(time.time()))
	time.sleep(1)

tracers = []
for r in new_routes:
	print(r)
	c.execute("INSERT INTO route VALUES('{0}',1)".format(r[0]))
	tracers.append(Popen(['python','route.py',r[0]]))
children = True
while children:
	for t in tracers:
		if t.poll() == None:
			chilren = True
			ccount += 1			
	sys.stdout.write('{0} tracers remain.\r'.format(ccount))
	time.sleep(1)
