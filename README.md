# ddos_simulation

DDoS simulation written in Python using "scapy" and "multiprocessing" libraries. Used for educational purposes

![Screenshot](https://i.imgur.com/f9yRPDP.png)



## Options:

There are 3 different DDoS attacks:

- Flood 

- Teardrop 

- Black nurse


You can set different options filling the "config.py" file:

- IP address

- Number of IPs

- Number of packets per IP

- Interface

- Type of attack

- Origin of IP addresses ("ips.txt" file or random addresses)

- Threads



## Requirements

Python 2.x:

```
pip install scapy
```

Python 3.x:

```
pip3 install scapy
```

## Note

Tested both in Python2.x (2.7.15rc1) and Python 3.x (3.6.7)
