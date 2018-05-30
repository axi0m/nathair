# author: axi0m
# purpose: rudimentary password cracker
# usage: crack.py
# changelog: 02/26/18 - initial creation
# 05/28/18 - migrated to hashlib module and updated to PEP8 format

import hashlib


def test_pass(cryptPass):
    salt = cryptPass[0:2]
    dictFile = open('dictionary.txt', 'r')
    for word in dictFile.readlines():
        word = word.strip('\n')
        digest = hashlib.sha256()
        digest.update(b'word')
        digest.digest()
        if (digest == cryptPass):
            print("[+] Found Password: " + word + "\n")
            return
    print("[-] Password Not Found.\n")
    return


def main():
    passFile = open('passwords.txt')
    for line in passFile.readlines():
        if ":" in line:
            user = line.split(':')[0]
            cryptPass = line.split(':')[1].strip(" ")
            print("[*] Cracking password for: " + user)
            test_pass(cryptPass)


if __name__ == "__main__":
    main()