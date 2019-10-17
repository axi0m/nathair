# author: axi0m
# purpose: banner grabber
# usage: ftp_banner_grabber.py <vuln banner file>
# changelog: 02/21/18 - initial creation
#            02/23/18 - minor updates and rename file
#            02/26/18 - adding vuln_banners.txt file to read in and iterate over, also changed name of script, had typo
#            05/29/18 - adding blank lines per PEP8, renaming functions per PEP8
#            10/17/19 - Per QL finding, adding handler for subclasses of BaseException - https://lgtm.com/rules/6780080/


import socket
import sys
import os
import logging
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
    with open("vuln_banners.txt", "r") as vuln_file:
        for line in vuln_file.readlines():
            if line.strip('\n') in banner:
                print(f"[+] Server is vulnerable! {banner}")


def main():
    if len(sys.argv) == 2:
        filename = sys.argv[1]
        if not os.path.isfile(filename):
            print(f"[!] ERROR {filename} does not exist!")
            exit(1)
        if not os.access(filename, os.R_OK):
            print(f"[!] ERROR {filename} Access Denied.")
            exit(1)
        else:
            print(f"[+] Reading Vulnerabilities From: {filename}")
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
