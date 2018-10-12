# author: axi0m
# purpose: rudimentary password cracker
# usage: crack.py
# changelog: 02/26/18 - initial creation
# 05/28/18 - migrated to hashlib module and updated to PEP8 format
# https://docs.python.org/3/library/hashlib.html
# 10/10/18 - added click as import to handle arguments better than argparse
'''

To do:
Add logging and be more verbose in the exception/error handling
Using `map` may be a better way than with for handling files

'''

import hashlib
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--passfile', nargs='?', default='F:\Password_Dump.txt', help="Password dump file", action="store", dest='passfile')
parser.add_argument('--hashtype', nargs='?', default='md5', help="The hash algorithm to use", action="store", dest='hashtype')
parser.add_argument('--hashfile', nargs='?', default='F:\Documents\Python\violent_python\crack\passwords.txt', action="store", dest='hashfile', help="The hashed password list to crack")

args = parser.parse_args()

passfile = args.passfile
hashtype = args.hashtype
hashfile = args.hashfile

def test_pass(hashtype, hashPass):
    # below code was in example when using crypt module which does not exist anymore
    # salt = cryptPass[0:2]
    with open(passfile, 'r') as dictFile:
        for word in dictFile:
            word = word.strip('\n')
            if hashtype == 'md5':
                digest = hashlib.md5(word.encode('utf-8'))
            if hashtype == 'sha256':
                digest = hashlib.sha256(word.encode('utf-8'))
                if (digest.hexdigest() == hashPass):
                    print("[+] Found Password: " + word + "\n")
                    return
        print("[-] Password Not Found.\n")
    return


def main(hashfile, hashtype):
    hashFile = open(hashfile)
    for line in hashFile.readlines():
        if ":" in line:
            user = line.split(':')[0]
            hashPass = line.split(':')[1].strip(" ")
            print("[*] Cracking password for: " + user)
            test_pass(hashtype, hashPass)


if __name__ == "__main__":
    main(hashfile, hashtype)