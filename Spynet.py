#!/usr/bin/env python

import argparse
import scapy.all as scapy
import socket
import sys
from datetime import datetime as dt
import os
Bold='\033[1m'
Red='\033[0;31m'
Green='\033[0;32m'
Blue='\033[0;94m'
Yellow='\033[0;93m'
NC='\033[0m' # No Color

os.system("clear")

print("\n" + Green + Bold)
print("  /$$$$$$                                            /$$")
print(" /$$__  $$                                          | $$  ")
print("| $$  \__/  /$$$$$$  /$$   /$$ /$$$$$$$   /$$$$$$  /$$$$$$  ")
print("|  $$$$$$  /$$__  $$| $$  | $$| $$__  $$ /$$__  $$|_  $$_/  ")
print("\____  $$| $$  \ $$| $$  | $$| $$  \ $$| $$$$$$$$  | $$    ")
print("/$$  \ $$| $$  | $$| $$  | $$| $$  | $$| $$_____/  | $$ /$$")
print("|  $$$$$$/| $$$$$$$/|  $$$$$$$| $$  | $$|  $$$$$$$  |  $$$$/")
print(" \______/ | $$____/  \____  $$|__/  |__/ \_______/   \___/")
print("          | $$       /$$  | $$")
print("          | $$      |  $$$$$$/")
print("          |__/       \______/   " + NC)
print("")
print("\t" + Red + "Made by: " + Bold + "Rival23 " + NC + Red + "and " + Bold + "Requird" + NC)
print("\n")
def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", dest="target", help="{+} networkaddr + submask ( e.g. 192.168.1.0/24)")
    options = parser.parse_args()
    if not options.target:
        parser.error("[-] Please specify a networkaddr with it's subnetmask. --help for more information")
    return options

def print_ports(host, ports):
    print("[+] host: " + host)
    for port in ports:
        print("\t[+] Open port: " + str(port))
def discover_host(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    client_list = []
    for answer in answered_list:
        client_ip = answer[1].psrc
        client_ip = str(client_ip)
        #print(client_ip)
        client_list.append(client_ip)

    return client_list

def discover_port(host):
    #gethostname
    target = socket.gethostbyname(host)
    ports = []
    try:
            for port in range(1, 1024):
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                socket.setdefaulttimeout(0.01)
                result = s.connect_ex((target, port))
                if result == 0:
                    protocolname = 'tcp'
                    service = socket.getservbyport(port, protocolname)
                    print(Yellow + "\t[+] Open port: " + Bold + str(port) + "\t" + service + NC)
                    ports.append(result)
                s.close()
            return ports
    except socket.error:
        print(Red + "[-] Couldn't connect to host." + NC)
    except KeyboardInterrupt:
        print(Blue + "[-] Skipping host: " + Bold + host + NC)
        return 0

def portscan_host(hosts):
    for host in hosts:
        print(Green + "[+] Port scan started for host: " + Bold +  host + NC)
        ports = discover_port(host)
        #print_ports(host, ports)

#parse arguments passed by user
options = get_arguments()

#scan for alive hosts in the range
host_results = discover_host(options.target)

#start portscan for each host alive and perform version and service scan
portscan_host(host_results)




#TODO Exclude Address
