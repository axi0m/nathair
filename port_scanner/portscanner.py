"""
Very helpful
TODO: https://gist.github.com/tonybaloney/8f36998f1bd552a61643668de47f1ba7
"""

import argparse
import asyncio
import logging
import multiprocessing as mp
import socket
from threading import Thread
from queue import Queue
import time
# from colorama import Fore, init

# init colorama
# init()

# default socket timeout
timeout = 1

def toggle_verbose(flag):
    ''' Toggle verbose logging on/off 
    
    :param flag: enable or disable logging in verbose(read DEBUG) mode
    '''

    if flag:
        logging.basicConfig(level='DEBUG')
        logging.debug('Logging in debug mode')


def tcp_connect_mp(host: str, port: int, results: mp.Queue):
    ''' TCP CONNECT and banner receiver (multiprocessing)

    :param host: IPv4 address of host to target
    :param port: TCP port of host to CONNECT to
    :param results: Queue to store our results
    '''

    socket.setdefaulttimeout(timeout)
    conn_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    with conn_socket as s:
        result = s.connect_ex((host, port))

        # TODO: Receiving banner data, decoding and displaying

        if result == 0:
            results.put(port)


def tcp_connect_threading(host: str, port: int, results: Queue):
    ''' TCP CONNECT and banner receiver (threading)

    :param host: IPv4 address of host to target
    :param port: TCP port of host to CONNECT to
    :param results: Queue to store our results
    '''
    socket.setdefaulttimeout(timeout)
    conn_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    with conn_socket as s:
        result = s.connect_ex((host, port))
        s.send(b"SampleData\r\n")
        banner = s.recv(100)
        decoded_banner = repr(banner)

        if result == 0:
            results.put(port)
            #banners.put(decoded_banner)
        

async def tcp_connect_async(host: str, port: int, results: list):
    """ TCP CONNECT and banner receiver (async)

    :param host: IPv4 address of host to target
    :param port: TCP port of host to CONNECT to
    :param results: List to store our results
    """
    try:
        future = asyncio.open_connection(host=host, port=port)
        r, w = await asyncio.wait_for(future, timeout=timeout)
        results.append(port)
        w.close()
    except asyncio.TimeoutError:
        # Port is closed
        pass


def convert_hostname(host):
    """ Wrapper for socket.gethostbyname to get IPv4 address

    :param host: DNS name or IPv4 address of host
    """

    try:
        targetipv4 = socket.gethostbyname(host)
        logging.debug(f'[*] Host IPv4 address resolved via DNS is {targetipv4}')
        return targetipv4

    except socket.error as sock_err:
        logging.error(f'[!] Socket error encountered: {sock_err}')
        return None

    except Exception as generic_err:
        logging.error(f'[!] Cannot resolve host {host}: {generic_err}')
        return None


def host_scan_mp(targetipv4, ports):
    """ Perform scan for given hostname and TCP port number(s)
    
    :param targetipv4: IPv4 of host to target
    :param ports: List of TCP ports to connect to
    """

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
            processes.append(pool.apply_async(tcp_connect_mp, (targetipv4, port, outputs)))
        for process in processes:
            process.get()
        while not outputs.empty():
            print("Port {0} is open".format(outputs.get()))


def host_scan_threading(targetipv4, ports):
    """ Perform scan given hostname and TCP port number(s) using threads

    :param targetipv4: IPv4 of host to target
    "param ports: List of TCP ports to connect to
    """

    # Init our threads list
    threads = []

    # Init our Queue object for storing results from threads
    results = Queue()

    # Start a thread for each port, pass func and args to thread
    for port in ports:
        t = Thread(target=tcp_connect_threading, args=(targetipv4, port, results))
        t.start()
        threads.append(t)

    # Join our threads together once all have terminated successfully
    for t in threads:
        t.join()
    
    # As the threads finish, the results queue object will grow in size, print the values of the queue
    while not results.empty():
        print('Port {0} is open'.format(results.get()))


async def host_scan_async(targetipv4, ports):
    """ Perform scan given hostname and TCP port number(s) using async coroutines

    :param targetipv4: IPv4 of host to target
    "param ports: List of TCP ports to connect to
    """

    tasks = []
    results = []
    for port in ports:
        tasks.append(tcp_connect_async(targetipv4, port, results))
    await asyncio.gather(*tasks)
    return results


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
    parser.add_argument(
        "--mode",
        action="store",
        dest="mode",
        help="Mode to operate in, using processes, threads or async functions. processes, threads, async are acceptable values."
    )

    # Parse our arguments into internal variables
    args = parser.parse_args()

    # Cleaner variable names
    host = args.host
    ports = args.ports
    examples = args.examples
    verbose_mode = args.verbose
    mode = args.mode
    
    if examples:
        print(
            '''
    ## EXAMPLES ##
    
    Scan a host on TCP port 22
        portscanner.py --host 192.168.1.1 --ports 22 --mode threads

    Scan a host on multiple TCP ports
        portscanner.py --host 192.168.1.1 --ports 9090, 443, 25 --mode processes
            '''
        )
        exit(0)

    # Check user provided us values for host and port(s)
    if host is None:
        parser.print_help()
        exit(0)

    if ports is None:
        parser.print_help()
        exit(0)

    # If user provides verbose, increase logging level, otherwise default to info
    if verbose_mode:
        toggle_verbose(True)
        print(verbose_mode)
    else:
        logging.basicConfig(level='ERROR')
        logging.info('Logging level in error mode (default)')
    
    # Check if user provided mode
    if mode is None:
        print(f'Provide mode to operate in: processes, threads, async')
        parser.print_help()
        exit(0)
    
    # Check if mode is viable option or not
    if mode != "threads" and mode != "processes" and mode != "async":
        print(f'Invalid mode provided, acceptable values are: processes, threads, async')
        parser.print_help()
        exit(0)
    
    # Remove the comma and space from list of ports
    stripped = [port.strip(', ') for port in ports]

    # Convert list of strings to list of integers
    integer_ports = [int(port) for port in stripped]

    # Convert provided host to IPv4
    targetipv4 = convert_hostname(host)

    # If mode is 'processes' use multiprocessing
    if mode == "processes":
        if targetipv4 and integer_ports:
            host_scan_mp(targetipv4, integer_ports)

    # If mode is 'threading' use threading
    if mode == "threads":
        if targetipv4 and integer_ports:
            host_scan_threading(targetipv4, integer_ports)

    # if mode is 'async' use async coroutines
    if mode == "async":
        if targetipv4 and integer_ports:
            results = asyncio.run(host_scan_async(targetipv4, integer_ports))
            for result in results:
                print("port {0} is open".format(result))

if __name__ == "__main__":
    start = time.perf_counter()
    main()
    stop = time.perf_counter()
    print(f'[*] Execution time was: {stop-start:0.4f} seconds')
