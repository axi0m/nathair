"""
Very helpful
https://gist.github.com/tonybaloney/8f36998f1bd552a61643668de47f1ba7
https://pythex.org/
"""

import argparse
import asyncio
import logging
import multiprocessing as mp
import socket
import sys
from queue import Queue
from rich.console import Console
from threading import Thread
from ipaddress import AddressValueError
from ipaddress import NetmaskValueError
from ipaddress import ip_network


# Initialize rich Console
console = Console()

# Set default socket timeout
timeout = 1

FORMAT = "%(filename)s:%(lineno)s - %(funcName)s() %(message)s"
logging.basicConfig(format=FORMAT)


def tcp_connect_mp(host: str, port: int, results: mp.Queue):
    """TCP CONNECT and banner receiver (multiprocessing)

    :param host: IPv4 address of host to target
    :param port: TCP port of host to CONNECT to
    :param results: Queue to store our results
    """

    socket.setdefaulttimeout(timeout)
    conn_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    with conn_socket as s:
        result = s.connect_ex((host, port))

        # TODO: Receiving banner data, decoding and displaying

        if result == 0:
            results.put(port)


def tcp_connect_threading(host: str, port: int, results: Queue):
    """TCP CONNECT and banner receiver (threading)

    :param host: IPv4 address of host to target
    :param port: TCP port of host to CONNECT to
    :param results: Queue to store our results
    """
    socket.setdefaulttimeout(timeout)
    conn_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    with conn_socket as s:
        result = s.connect_ex((host, port))
        try:
            s.send(b"SampleData\r\n")
            # banner = s.recv(100)
            if result == 0:
                results.put(port)
        except socket.timeout as e:
            logging.debug(
                f"[!] Connection timed out, port {port} is closed or host {host} is down: {e}"
            )
            return False
        except ConnectionResetError as e:
            logging.debug(f"[!] Connection reset by peer {host} on port {port}")
            return False
        except BrokenPipeError as e:
            logging.debug(
                f"[!] Broken pipe error, usually this means thread terminated while writes were still pending: {e}"
            )
            return False


async def tcp_connect_async(host: str, port: int, results: list):
    """TCP CONNECT and banner receiver (async)

    :param host: IPv4 address of host to target
    :param port: TCP port of host to CONNECT to
    :param results: List to store our results
    """
    try:
        future = asyncio.open_connection(host=host, port=port)
        r, w = await asyncio.wait_for(future, timeout=timeout)
        results.append(port)
        w.close()
        r.close()
    except asyncio.TimeoutError:
        # Port is closed
        pass


def convert_hostname(host):
    """Wrapper for socket.gethostbyname to get IPv4 address

    :param host: DNS name or IPv4 address of host
    """

    try:
        targetipv4 = socket.gethostbyname(host)
        logging.debug(f"[*] Host IPv4 address resolved via DNS is {targetipv4}")
        return targetipv4

    except socket.error as sock_err:
        logging.error(f"[!] Socket error encountered: {sock_err}")
        return None

    except Exception as generic_err:
        logging.error(f"[!] Cannot resolve host {host}: {generic_err}")
        return None


def generate_hosts(host: str) -> list:
    """Return list of hosts from CIDR

    :param host: Hosts in CIDR format
    """
    try:
        network = ip_network(host)
        logging.debug(f"[+] CIDR is valid for provided target host: {host}")
        return list(network.hosts())

    except AddressValueError as val_error:
        logging.error(f"[!] Invalid address provided: {host}")
        return None

    except NetmaskValueError as mask_error:
        logging.error(f"[!] Invalid netmask provided: {host}")
        return None

    except Exception as generic_err:
        logging.error(f"[!] Exception occurred: {generic_err}")
        return None


def host_scan_mp(targetipv4, ports):
    """Perform scan for given hostname and TCP port number(s)

    :param targetipv4: IPv4 of host to target
    :param ports: List of TCP ports to connect to
    """

    # Initialize empty list of processes
    processes = []

    # Tell multiprocessing to use spawn method
    try:
        mp.set_start_method("spawn")
    except RuntimeError as e:
        pass

    # Init our process pool manager
    pool_manager = mp.Manager()

    # For each port, we'll create a new process to tcp_connect
    with mp.Pool(len(ports)) as pool:

        # Create a queue object for the output of our processes
        outputs = pool_manager.Queue()

        # For each port we'll spawn a process to run our function
        for port in ports:
            processes.append(
                pool.apply_async(tcp_connect_mp, (targetipv4, port, outputs))
            )
        for process in processes:
            process.get()
        while not outputs.empty():
            console.print(
                f"[+] Port [blue]{outputs.get()}[/blue] is open for host [blue]{targetipv4}[/blue]",
                style="bold green",
            )


def host_scan_threading(targetipv4, ports):
    """Perform scan given hostname and TCP port number(s) using threads

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
        console.print(
            f"[+] Port [blue]{results.get()}[/blue] is open for host [blue]{targetipv4}[/blue]",
            style="bold green",
        )


async def host_scan_async(targetipv4, ports):
    """Perform scan given hostname and TCP port number(s) using async coroutines

    :param targetipv4: IPv4 of host to target
    :param ports: List of TCP ports to connect to
    """

    tasks = []
    results = []
    for port in ports:
        tasks.append(tcp_connect_async(targetipv4, port, results))
    await asyncio.gather(*tasks, return_exceptions=True)
    return results


def main():
    """Main function to parse arguments and run port scan"""
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
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")
    parser.add_argument("--version", action="version", version="{prog} + {__version__}")
    parser.add_argument(
        "--examples", action="store_true", help="Display examples and exit"
    )
    parser.add_argument(
        "--mode",
        action="store",
        dest="mode",
        help="Mode to operate in, using processes, threads or async functions. processes, threads, async are acceptable values.",
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
        console.print(
            """
    ## EXAMPLES ##

    Scan a host on TCP port 22
        portscanner.py --host 192.168.1.1 --ports 22 --mode threads

    Scan a host on multiple TCP ports
        portscanner.py --host 192.168.1.1 --ports 9090, 443, 25 --mode processes
            """,
            style="bold green",
        )
        sys.exit(0)

    # Check user provided values for host and port(s)
    if host is None:
        parser.print_help()
        sys.exit(0)

    if ports is None:
        parser.print_help()
        sys.exit(0)

    # If user provides verbose, increase logging level, otherwise default to info
    if verbose_mode:
        console.print(f"[-] Enabled verbose_mode")
        logging.basicConfig(level="DEBUG")
        logging.debug("Logging in debug mode")
    else:
        console.print(f"[-] Standard logging mode enabled")
        logging.basicConfig(level="ERROR")
        logging.info("Logging level in error mode (default)")

    # Check if user provided mode
    if mode is None:
        console.print(
            f"[!] Provide mode to operate in: processes, threads, async",
            style="bold yellow",
        )
        parser.print_help()
        sys.exit(0)

    # Check if mode is viable option or not
    if mode != "threads" and mode != "processes" and mode != "async":
        console.print(
            f"[!] Invalid mode provided, acceptable values are: processes, threads, async",
            style="bold yellow",
        )
        parser.print_help()
        sys.exit(0)

    # Remove the comma and space from list of ports
    stripped = [port.strip(", ") for port in ports]

    # Convert list of strings to list of integers
    integer_ports = [int(port) for port in stripped]

    # If CIDR format suspected, pass to generate_hosts
    if "/" in host:
        console.print(f"[-] Slash detected in user provided host: {host}")
        logging.debug(f"[-] Possible CIDR range provided as target host: {host}")
        targethosts = generate_hosts(host)

        # If mode is 'processes' use multiprocessing
        if mode == "processes":
            logging.debug(f"Begin multiprocessing mode...")
            logging.debug(f"List of target hosts provided")
            if integer_ports:
                for singlehost in targethosts:
                    host_scan_mp(str(singlehost), integer_ports)

        # If mode is 'threading' use threading
        if mode == "threads":
            logging.debug(f"Begin multithreading mode...")
            logging.debug(f"List of target hosts provided")
            if integer_ports:
                for singlehost in targethosts:
                    host_scan_threading(str(singlehost), integer_ports)

        # if mode is 'async' use async coroutines
        if mode == "async":
            logging.debug(f"Begin async mode...")
            logging.debug(f"List of target hosts provided")
            if integer_ports:
                for singlehost in targethosts:
                    results = asyncio.run(
                        host_scan_async(str(singlehost), integer_ports)
                    )
                    for result in results:
                        console.print(
                            f"[+] Port [blue]{result}[/blue] is open for host [blue]{singlehost}[/blue]",
                            style="bold green",
                        )

    # If the host is not a CIDR format, assume it is a single host and convert to IPv4 address
    else:
        console.print(f"[-] No slash detected in user provided host, not CIDR: {host}")
        logging.debug(f"No slash detected in user provided host, not CIDR: {host}")
        targetipv4 = convert_hostname(host)

        # If mode is 'processes' use multiprocessing
        if mode == "processes":
            logging.debug(f"Begin multiprocessing mode...")
            logging.debug(f"Individual target host provided")
            if integer_ports:
                host_scan_mp(targetipv4, integer_ports)

        # If mode is 'threading' use threading
        if mode == "threads":
            logging.debug(f"Begin multithreading mode...")
            logging.debug(f"Individual target host provided")
            if integer_ports:
                host_scan_threading(targetipv4, integer_ports)

        # if mode is 'async' use async coroutines
        if mode == "async":
            results = asyncio.run(host_scan_async(targetipv4, integer_ports))
            for result in results:
                console.print(
                    f"[+] Port [blue]{result}[/blue] is open for host [blue]{targetipv4}[/blue]",
                    style="bold green",
                )


if __name__ == "__main__":
    main()
