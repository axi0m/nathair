# author: axi0m
# purpose: rudimentary port scanner (TCP CONNECT port scan)
# usage: portscanner.py --host --port
# example: portscanner.py --host 10.1.1.1 --port 21,22,23
# changelog: 12/11/18 - initial creation
# 12/12/2018 - added threading, fixed functions up a bit, fixed byte
# format for socket data 

'''

To do:
Add the following scan types
TCP SYN, TCP XMAS, TCP FIN, TCP NULL, TCP SYN
https://nmap.org/book/man-port-scanning-techniques.html

Add Unit Tests
Add Logging
Add Colorized Output via colorama
Add pprint type functionality
Add output via JSON

Weird bug in recv from port 22, results are returned and are bytes but for w/e 
reason the CLI hangs and never completes. Blocking mode issue?

'''

import argparse
import socket
import threading
import sys
import logging

screenLock = threading.Semaphore(value=1)

def connScan(host, port):
    try:
        socket.setdefaulttimeout(1)
        connSocket = socket.socket()
        connSocket.connect((host, port))
        connSocket.send('SampleData\r\n'.encode('utf-8'))
        results = connSocket.recv(100)
        screenLock.acquire()
        print("[+] {}/tcp open".format(port))
        print("[+] {}".format(results.decode('utf-8')))

    except TimeoutError:
        screenLock.acquire()
        print("[!] Connection timeout on port {}".format(port))

    except Exception as e:
        logging.error("Exception while trying to connect: {}".format(e))
        screenLock.acquire()
        print("[-] {}/tcp closed".format(port))

    finally:
        screenLock.release()
        connSocket.close()


def portScan(host, port):
    try:
        targetipv4 = socket.gethostbyname(host)
    except Exception as e:
        print("[!] Cannot resolve {}".format(host))
        return
    try:
        targetname = socket.gethostbyaddr(host)
        print("\nScan Results for: {}".format(targetname[0]))
    except Exception as e:
        logging.error("Exception encountered during address resolution: {}".format(e))
        print("\nScan Results for: {}".format(targetipv4))

    socket.setdefaulttimeout(1)

    for i in port:
        t = threading.Thread(target=connScan, args=(host, int(i)))
        t.start()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', nargs='?', action="store", dest='host', help="Host to scan.")
    parser.add_argument('--port', nargs='+', action="store", dest="port", help="Port(s) to scan, csv and space delimited")

    args = parser.parse_args()

    host = args.host
    port = args.port

    if host is None or port is None:
        parser.print_help()
        sys.exit(0)
    portScan(host, port)


if __name__ == '__main__':
    main()
