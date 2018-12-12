# author: axi0m
# purpose: rudimentary port scanner
# usage: portscanner.py --host --port
# example: portscanner.py --host 10.1.1.1 --port 21,22,23
# changelog: 12/11/18 - initial creation
'''

To do:

'''

import argparse
from socket import *

parser = argparse.ArgumentParser()
parser.add_argument('--host', nargs='?', action="store", dest='host', help="Host to scan.")
parser.add_argument('--port', nargs='+', action="store", dest="port", help="Port(s) to scan, csv delimited")

args = parser.parse_args()

host = args.host
port = args.port

if (host == None) | (port == None):
    parser.print_help()
    exit(0)

def connScan(host, port):
    try: 
        connSocket = socket(AF_INET, SOCK_STREAM)
        connSocket.connect((host, port))
        print("[+]{}/tcp open".format(port))
        connSocket.close()
    except:
        print("[-] {}/tcp closed".format(port))

def portScan(host, port):
    try:
        targetipv4 = gethostbyname(host)
    except:
        print("[!] Cannot resolve {}".format(host))
        return
    try:
        targetname = gethostbyaddr(host)
        print("\n[+] Scan Results for : {}".format(targetname[0]))
    except:
        print("\n[+] Scan Results for : {}".format(targetipv4))

def main():
    setdefaulttimeout(5)

    for i in port:
        print("Scanning port {}".format(i))
        connScan(host, int(i))

if __name__ == '__main__':
    main()