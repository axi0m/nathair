# author: axi0m
# purpose: rudimentary port scanner (TCP CONNECT port scan)
# usage: portscanner.py --host --port
# example: portscanner.py --host 10.1.1.1 --port 21,22,23
# changelog: 12/11/18 - initial creation
# 12/12/2018 - added threading, fixed functions up a bit, fixed byte format for socket data 
'''

To do:
Add the following scan types
TCP SYN, TCP XMAS, TCP FIN, TCP NULL, TCP SYN
https://nmap.org/book/man-port-scanning-techniques.html

Weird bug in recv from port 22, results are returned and are bytes but for w/e reason the CLI hangs and never completes. Blocking mode issue?

'''

import argparse
import socket
from threading import *
from socket import *
import sys

screenLock = Semaphore(value=1)

def connScan(host, port):
    try:
        setdefaulttimeout(1)
        connSocket = socket(AF_INET, SOCK_STREAM)
        connSocket.connect((host, port))
        connSocket.send('SampleData\r\n'.encode('utf-8'))
        results = connSocket.recv(100)
        screenLock.acquire()
        print("[+] {}/tcp open".format(port))
        print("[+] {}".format(results.decode('utf-8')))

    except TimeoutError:
        screenLock.acquire()
        print("[!] Connection timeout on port {}".format(port))

    except:
        screenLock.acquire()
        print("[-] {}/tcp closed".format(port))

    finally:
        screenLock.release()
        connSocket.close()

def portScan(host, port):
    try:
        targetipv4 = gethostbyname(host)
    except:
        
        print("[!] Cannot resolve {}".format(host))
        return
    try:
        targetname = gethostbyaddr(host)
        print("\nScan Results for: {}".format(targetname[0]))
    except:
        print("\nScan Results for: {}".format(targetipv4))

    setdefaulttimeout(1)

    for i in port:
        #print("[!] Scanning port {}...".format(i)) # Not sure how we do this with threads?
        t = Thread(target=connScan, args=(host, int(i)))
        t.start()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', nargs='?', action="store", dest='host', help="Host to scan.")
    parser.add_argument('--port', nargs='+', action="store", dest="port", help="Port(s) to scan, csv delimited")

    args = parser.parse_args()

    host = args.host
    port = args.port

    if (host == None) | (port == None):
        parser.print_help()
        sys.exit(0)
    portScan(host, port)

if __name__ == '__main__':
    main()