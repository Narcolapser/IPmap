from traceroute.traceroute import Traceroute
import subprocess
import sys
import sqlite3
import random
import time

ip = sys.argv[1]

print(ip)

tr = Traceroute(ip)
hops = tr.traceroute()

db = sqlite3.connect("ipmap.db")
c = db.cursor()
c.execute("CREATE TABLE IF NOT EXISTS step(dest TEXT, step TEXT, step_num INT)")
query = "INSERT INTO step VALUES('{0}','{1}',{2})"
for i in hops:
	written = False
	while not written:
		try:
			c.execute(query.format(ip,i['ip_address'],i['hop_num']))
			print(query.format(ip,i['ip_address'],i['hop_num']))
			written = True
		except:
			time.sleep(random.random()*10)
	
db.commit()

