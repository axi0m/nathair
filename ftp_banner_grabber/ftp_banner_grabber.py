# author: axi0m
# purpose: banner grabber
# usage: ftp_banner_grabber.py <vuln banner file>

import socket
import os
import argparse
import ipaddress
from colorama import Fore, init

# init colorama
init()


def ret_banner(ip, port):
    try:
        socket.setdefaulttimeout(2)
        s = socket.socket()
        s.connect((ip, port))
        print(
            Fore.YELLOW
            + f"[+] Established network connection with host {ip} using port {port}"
        )
        banner = s.recv(1024)
        return f"{banner}"

    except SystemExit as sys_exit:
        print(
            Fore.LIGHTYELLOW_EX + f"[!] ERROR operation failed, system exit: {sys_exit}"
        )
        return None

    except KeyboardInterrupt as keybd_err:
        print(
            Fore.LIGHTYELLOW_EX
            + f"[!] ERROR operation canceled via Keyboard Interrupt: {keybd_err}"
        )
        return None

    except Exception as generic_err:
        print(
            Fore.LIGHTYELLOW_EX
            + f"[!] ERROR unable to establish socket connection to IP address {ip} on TCP port {port}: {generic_err}"
        )
        return None


def check_vulns(reference_file, test_banner):
    with open(reference_file, "r") as ref_file:
        for line in ref_file.readlines():
            if line.strip("\n") in test_banner:
                print(Fore.GREEN + f"[+] Server is vulnerable! {test_banner}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--file",
        nargs="?",
        action="store",
        dest="vulnfile",
        help="Filename with vulnerable banners to match against",
    )
    parser.add_argument(
        "--range",
        nargs="?",
        action="store",
        dest="iprange",
        help="IPv4 address range to scan in CIDR form: i.e. 192.168.1.0/24",
    )
    parser.add_argument(
        "--ports",
        nargs="+",
        action="store",
        dest="ports",
        help="Space separated list of ports to check",
    )

    args = parser.parse_args()

    vulnerable_banner_file = args.vulnfile
    target_ipv4_range = args.iprange

    # Ensure we have target IPv4 range
    if not target_ipv4_range:
        print(
            Fore.LIGHTYELLOW_EX
            + f"[!] ERROR - You must provide an IPv4 range in CIDR notation!"
        )
        parser.print_help()
        exit(1)

    # Use IPAddress module to parse CIDR range and validate it
    network_hosts = ipaddress.ip_network(target_ipv4_range)

    # Use temporary variable for parsed ports parameter
    target_ports = args.ports

    # Ensure we were provided port(s) to check
    if not target_ports:
        print(Fore.LIGHTYELLOW_EX + f"[!] ERROR - Port list not provided")
        parser.print_help()
        exit(1)

    # Ensure we were provided a file as parameter
    if not vulnerable_banner_file:
        print(Fore.LIGHTYELLOW_EX + f"[!] ERROR - Vulnerable banner file not provided")
        parser.print_help()
        exit(1)

    # Ensure file exists
    if not os.path.isfile(vulnerable_banner_file):
        print(
            Fore.LIGHTYELLOW_EX
            + f"[!] ERROR - {vulnerable_banner_file} does not exist!"
        )
        exit(1)

    # Ensure we can read the file
    if not os.access(vulnerable_banner_file, os.R_OK):
        print(
            Fore.LIGHTYELLOW_EX + f"[!] ERROR - {vulnerable_banner_file} Access Denied."
        )
        exit(1)

    print(
        Fore.YELLOW
        + f"[+] INFO - Reading vulnerabilities from: {vulnerable_banner_file}"
    )

    # .hosts() method creates a generator for all our hosts in the network
    for ip in network_hosts.hosts():
        for port in target_ports:
            # Must convert ip to String for ret_banner function instead of IPv4Address type
            string_ip = str(ip)
            # Must convert port from str to integer for ret_banner function
            int_port = int(port)
            # Get the banner from the remote host and store as string to compare
            banner = ret_banner(string_ip, int_port)
            if banner:
                # Easier to strip it of erroneous characters before comparing
                stripped_banner = banner.strip("\r\n")
                # DEBUG print(f"[+] {ip}:{port} {stripped_banner}")
                check_vulns(vulnerable_banner_file, stripped_banner)


if __name__ == "__main__":
    main()
