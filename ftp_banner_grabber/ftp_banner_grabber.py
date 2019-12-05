# author: axi0m
# purpose: banner grabber
# usage: ftp_banner_grabber.py <vuln banner file>

import socket
import sys
import os
import argparse

def ret_banner(ip, port):
    try:
        socket.setdefaulttimeout(2)
        s = socket.socket()
        s.connect((ip, port))
        print(f"[+] Established network connection with host {ip} using port {port}")
        banner = s.recv(1024)
        return f"{banner}"

    except SystemExit as sys_exit:
        print(f"[!] ERROR operation failed, system exit: {sys_exit}")
        return None

    except KeyboardInterrupt as keybd_err:
        print(f"[!] ERROR operation canceled via Keyboard Interrupt: {keybd_err}")
        return None

    except Exception as generic_err:
        print(f"[!] ERROR unable to establish socket connection to IP address {ip} on TCP port {port}: {generic_err}")
        return None


def check_vulns(banner):
    with open(banner, "r") as vuln_file:
        for line in vuln_file.readlines():
            if line.strip('\n') in banner:
                print(f"[+] Server is vulnerable! {banner}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file',nargs='?',action='store',dest='vulnfile',help="Filename with vulnerable banners to match against")
    
    args = parser.parse_args()

    vulnerable_banner_file = args.vulnfile
    
    # Ensure we were provided a file as parameter
    if not vulnerable_banner_file:
        print(f'[!] ERROR vulnerable banner file not provided')
        parser.print_help()

    # Ensure file exists
    if not os.path.isfile(vulnerable_banner_file):
        print(f"[!] ERROR {vulnerable_banner_file} does not exist!")
        exit(1)
    
    # Ensure we can read the file
    if not os.access(vulnerable_banner_file, os.R_OK):
        print(f"[!] ERROR {vulnerable_banner_file} Access Denied.")
        exit(1)

    print(f"[+] Reading vulnerabilities from: {vulnerable_banner_file}")
    portList = [21]
    for x in range(1, 10):
        ip = '192.168.1.' + str(x)
        for port in portList:
            banner = ret_banner(ip, port)
            if banner:
                stripped_banner = banner.strip('\r\n')
                print(f"[+] {ip}:{port} {stripped_banner}")
                check_vulns(stripped_banner)


if __name__ == '__main__':
    main()
