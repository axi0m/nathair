# author: axi0m
# purpose: rudimentary port scanner (TCP CONNECT port scan)
# usage: portscanner.py --host --port
# example: portscanner.py --host 10.1.1.1 --port 21,22,23

"""

TODO: Add the following scan types
TODO: TCP SYN, TCP XMAS, TCP FIN, TCP NULL, TCP SYN
TODO: https://nmap.org/book/man-port-scanning-techniques.html

TODO: Add Unit Tests
TODO: Add output via JSON

"""

import argparse
import socket
import threading
import logging
from colorama import Fore, init

# init colorama
init()

# init threading
SCREEN_LOCK = threading.Semaphore(value=1)


def toggle_verbose(flag):
    ''' Toggle verbose logging on/off 
    
    :param flag: enable or disable logging in verbose(read DEBUG) mode
    '''

    if flag:
        logging.basicConfig(level='DEBUG')
        logging.debug('Logging in debug mode')


def conn_scan(host, port):
    ''' TCP scan and banner receiver

    :param host: IPv4 address of host to target
    :param port: TCP port of host to CONNECT to
    '''

    socket.setdefaulttimeout(1)
    conn_socket = socket.socket()

    try:
        with conn_socket as s:
            s.connect((host, port))
            s.send(b"SampleData\r\n")
            results = s.recv(100)
            #decoded_results = results.decode('utf-8')
            decoded_results = repr(results)

        SCREEN_LOCK.acquire()

        print(Fore.GREEN + f"[+] {port}/tcp open")
        logging.info(f'[+] {port}/tcp open')

        print(Fore.GREEN + f"[+] {decoded_results}")
        logging.info(f"[+] {decoded_results}")

    except TimeoutError as timeout_error:
        SCREEN_LOCK.acquire()
        logging.error(f'[!] Connection timeout on port {port}: {timeout_error}')

    except KeyboardInterrupt as keybd_err:
        SCREEN_LOCK.acquire()
        logging.error(f'[!] Keyboard interrupt: {keybd_err}')

    except Exception as generic_err:
        SCREEN_LOCK.acquire()
        print(
            Fore.LIGHTYELLOW_EX
            + f"[-] Generic exception port most likely closed or network timeout: {generic_err}"
        )
        print(Fore.LIGHTYELLOW_EX + f"[-] {port}/tcp closed")
        logging.info(f'[-] {port}/tcp closed')

    finally:
        SCREEN_LOCK.release()


def port_scan(host, port):
    """ Perform scan for given hostname and TCP port number(s)"""
    try:
        targetipv4 = socket.gethostbyname(host)
        logging.debug(f'[*] Host IPv4 address resolved via DNS is {targetipv4}')

    except KeyboardInterrupt as keybd_err:
        logging.error(f'[!] Keyboard interrupt handled: {keybd_err}')
        return None

    except Exception as generic_err:
        logging.error(f'[!] Cannot resolve host {host}: {generic_err}')
        return None

    if targetipv4 is not None:
        try:
            targetname = socket.gethostbyaddr(host)
            logging.debug(f'[*] DNS result: {targetname[0]}')
        except Exception as generic_err:
            logging.error(f'[!] Exception encountered during address resolution: {generic_err}')

        socket.setdefaulttimeout(1)

        for tcp_port in port:
            thread_object = threading.Thread(
                target=conn_scan, args=(host, int(tcp_port))
            )
            thread_object.start()


def main():
    """ Main function to parse arguments and run port scan"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--host", nargs="?", action="store", dest="host", help="Host to scan."
    )
    parser.add_argument(
        "--port",
        nargs="+",
        action="store",
        dest="port",
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
    port = args.port
    examples = args.examples
    verbose_mode = args.verbose
    
    if examples:
        print(
            '''
    ## EXAMPLES ##
    
    Scan a host on TCP port 22
        portscanner.py --host 192.168.1.1 --port 22

    Scan a host on multiple TCP ports
        portscanner.py --host 192.168.1.1 --port 9090, 443, 25
            '''
        )
        exit(0)

    if host is None:
        parser.print_help()
        exit(0)

    if port is None:
        parser.print_help()
        exit(0)

    if verbose_mode:
        toggle_verbose(True)
        print(verbose_mode)
    else:
        logging.basicConfig(level='ERROR')
        logging.info('Logging level in error mode (default)')

    port_scan(host, port)


if __name__ == "__main__":
    main()
