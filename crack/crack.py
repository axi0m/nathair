#!/usr/bin/python3
# purpose: rudimentary password cracker
# usage: crack.py --passfile 'C:\password_dump.txt' --hashtype 'md5' --hashfile 'C:\captured_hashes.txt'
"""

TODO: Add logging and be more verbose in the exception/error handling
TODO: Add examples, debug and version parameters

"""

import hashlib
import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument(
    "--passfile",
    nargs="?",
    default="passwords_to_crack.txt",
    help="Password dump file",
    action="store",
    dest="passfile",
)
parser.add_argument(
    "--hashtype",
    nargs="?",
    default="md5",
    help="The hash algorithm to use",
    action="store",
    dest="hashtype",
)
parser.add_argument(
    "--hashfile",
    nargs="?",
    default="hashed_passwords.txt",
    action="store",
    dest="hashfile",
    help="The hashed password list to crack",
)
parser.add_argument(
    "--version",
    action="version",
    version="crack v0.1",
    help="Print the current version of the program",
)
parser.add_argument(
    "--examples",
    action="store_true",
    help="Print examples of running the program",
)
parser.add_argument(
    "--debug", action="store_true", help="Toggle debug level logging to console"
)

args = parser.parse_args()

# Easier to work with cleaner variable names
passfile = args.passfile
hashtype = args.hashtype
hashfile = args.hashfile
examples = args.examples
debug_mode = args.debug


def test_pass(hashtype, hashPass):
    """ Test if we hash of the password matches our password hash file """
    with open(passfile, "r") as dictFile:
        for word in dictFile:
            word = word.strip("\n")
            try:
                # TODO: If we create a new instance of the class I can dynamically update the hashtype as a passed variable
                # TODO: https://pymotw.com/2/hashlib/ <--- See that for details
                digest = hashlib.new(hashtype)
                digest.update(word.encode("utf-8"))

            except KeyboardInterrupt as keybd_err:
                print(f"[!] ERROR - Keyboard interrupt handled: {keybd_err}")

            except SystemExit as sys_exit:
                print(f"[!] ERROR - System exit: {sys_exit}")

            except Exception as generic_err:
                print(f"[!] ERROR - Generic exception encountered: {generic_err}")

            if digest.hexdigest() == hashPass:
                return print(f"[+] DEBUG - Found Password: {word}")
            else:
                return print(f"[-] DEBUG - Password Not Found.")


def main(hashfile, hashtype):
    """ Accept file of hashes and given hash type """

    if examples:
        print(f"Run crack.py against md5 Linux /etc/passwd file format\n")
        print(f"crack.py --hashtype md5 --hashfile passwd --passfile dictionary.txt")
        sys.exit(1)

    if debug_mode:
        print(f"[*] DEBUG - Selected hash algorithm: {hashtype}")

    with open(hashfile) as hashFile:
        for line in hashFile.readlines():
            if ":" in line:
                user = line.split(":")[0]
                hashPass = line.split(":")[1].strip(" ")
                if debug_mode:
                    print(f"[*] DEBUG - Cracking password for: {user}")
                test_pass(hashtype, hashPass)


if __name__ == "__main__":
    main(hashfile, hashtype)
