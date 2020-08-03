# author: axi0m
# purpose: rudimentary port scanner (TCP CONNECT port scan)
# usage: portscanner.py --host --ports
# example: portscanner.py --host 10.1.1.1 --ports 21, 22, 23

"""

TODO: Add the following scan types
TODO: TCP SYN, TCP XMAS, TCP FIN, TCP NULL, TCP SYN
TODO: https://nmap.org/book/man-port-scanning-techniques.html

TODO: Add Unit Tests
TODO: Add output via JSON
TODO: Support ranges in argparse --ports parameter
TODO: Add IPv6 support, getaddrinfo instead of gethostbyname
TODO: Add mode function - toggle between threading, multiprocessing and asyncio

Very helpful
TODO: https://gist.github.com/tonybaloney/8f36998f1bd552a61643668de47f1ba7

"""

import argparse
import logging
import multiprocessing as mp
import socket
import threading
import time
from colorama import Fore, init

# init colorama
init()

# default socket timeout
timeout = 1

def toggle_verbose(flag):
    ''' Toggle verbose logging on/off 
    
    :param flag: enable or disable logging in verbose(read DEBUG) mode
    '''

    if flag:
        logging.basicConfig(level='DEBUG')
        logging.debug('Logging in debug mode')


def tcp_connect(host: str, port: int, results: mp.Queue):
    ''' TCP CONNECT and banner receiver

    :param host: IPv4 address of host to target
    :param port: TCP port of host to CONNECT to
    :param results: Queue to store our results
    '''

    socket.setdefaulttimeout(timeout)
    conn_socket = socket.socket()

    with conn_socket as s:
        result = s.connect_ex((host, port))

        # TODO: Receiving banner data, decoding and displaying
        #s.send(b"SampleData\r\n")
        #results = s.recv(100).decode()

        if result == 0:
            results.put(port)

    #     print(Fore.GREEN + f"[+] {port}/tcp open")
    #     logging.info(f'[+] {port}/tcp open')

    #     print(Fore.GREEN + f"[+] {results}")
    #     logging.info(f"[+] {results}")

    # except TimeoutError as timeout_error:
    #     logging.error(f'[!] Connection timeout on port {port}: {timeout_error}')

    # except KeyboardInterrupt as keybd_err:
    #     logging.error(f'[!] Keyboard interrupt: {keybd_err}')

    # except Exception as generic_err:
    #     print(
    #         Fore.LIGHTYELLOW_EX
    #         + f"[-] Generic exception port most likely closed or network timeout: {generic_err}"
    #     )
    #     print(Fore.LIGHTYELLOW_EX + f"[-] {port}/tcp closed")
    #     logging.info(f'[-] {port}/tcp closed')

def convert_hostname(host):
    try:
        targetipv4 = socket.gethostbyname_ex(host)
        logging.debug(f'[*] Host IPv4 address resolved via DNS is {targetipv4}')
        return targetipv4

    except socket.error as sock_err:
        logging.error(f'[!] Socket error encountered: {sock_err}')
        return None

    except Exception as generic_err:
        logging.error(f'[!] Cannot resolve host {host}: {generic_err}')
        return None

def host_scan(targetipv4, ports):
    """ Perform scan for given hostname and TCP port number(s)
    
    :param targetipv4: IPv4 of host to target
    :param ports: List of TCP ports to connect to
    """

    # Set start time
    start = time.time()

    # Initialize empty list of processes
    processes = []

    # Tell multiprocessing to use spawn method
    mp.set_start_method('spawn')

    # Init our process pool manager
    pool_manager = mp.Manager()

    # For each port, we'll create a new process to tcp_connect
    with mp.Pool(len(ports)) as pool:

        # Create a queue object for the output of our processes
        outputs = pool_manager.Queue()

        # For each port we'll spawn a process to run our function
        for port in ports:
            processes.append(pool.apply_async(tcp_connect, (targetipv4, port, outputs)))
        for process in processes:
            process.get()
        while not outputs.empty():
            print("Port {0} is open".format(outputs.get()))
        print("Completed scan in {0} seconds".format(time.time() - start))

def main():
    """ Main function to parse arguments and run port scan"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--host", nargs="?", action="store", dest="host", help="Host to scan."
    )
    parser.add_argument(
        "--ports",
        nargs="+",
        action="store",
        dest="ports",
        help="Port(s) to scan, csv and space delimited",
    )
    parser.add_argument(
        "--verbose", 
        action="store_true", 
        help="Enable verbose logging"
    )
    parser.add_argument(
        "--version", 
        action="version", 
        version="{prog} + {__version__}"
    )
    parser.add_argument(
        "--examples", 
        action="store_true", 
        help="Display examples and exit"
    )

    args = parser.parse_args()

    host = args.host
    ports = args.ports
    examples = args.examples
    verbose_mode = args.verbose
    
    if examples:
        print(
            '''
    ## EXAMPLES ##
    
    Scan a host on TCP port 22
        portscanner.py --host 192.168.1.1 --ports 22

    Scan a host on multiple TCP ports
        portscanner.py --host 192.168.1.1 --ports 9090, 443, 25
            '''
        )
        exit(0)

    if host is None:
        parser.print_help()
        exit(0)

    if ports is None:
        parser.print_help()
        exit(0)

    if verbose_mode:
        toggle_verbose(True)
        print(verbose_mode)
    else:
        logging.basicConfig(level='ERROR')
        logging.info('Logging level in error mode (default)')
    
    # Remove the comma and space from list of ports
    stripped = [port.strip(', ') for port in ports]

    # Convert list of strings to list of integers
    integer_ports = [int(port) for port in stripped]

    # Convert provided host to IPv4
    targetipv4 = convert_hostname(host)

    # Pass host and list of ports to connect to
    if targetipv4 and integer_ports:
        host_scan(targetipv4, integer_ports)


if __name__ == "__main__":
    start = time.perf_counter()
    main()
    stop = time.perf_counter()
    print(f'[*] Execution time was: {start-stop:0.4f} seconds')
