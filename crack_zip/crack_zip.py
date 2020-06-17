# author: axi0m
# purpose: rudimentary zip cracker

import argparse
import pyzipper
import zipfile
import sys
import os
import logging

from colorama import Fore, init

# init colorama
init()

# init logging
logging.basicConfig(level='INFO')

parser = argparse.ArgumentParser()
parser.add_argument(
    "--file", nargs="?", action="store", dest="file", help="The zip file to crack."
)
parser.add_argument(
    "--pwdfile",
    nargs="?",
    action="store",
    dest="pwdfile",
    help="The reference password file.",
)

# Parse our arguments provided at CLI
args = parser.parse_args()

# Verify the variables were provided or print help
if not args.file:
    parser.print_help()
    exit(1)

if not args.pwdfile:
    parser.print_help()
    exit(1)

# Set to cleaner variable names for ease later on
zfile = args.file
pfile = args.pwdfile


def test_pyzipper():
    ''' Test if pyzipper is installed '''

    if 'pyzipper' not in sys.modules:
        logging.info(f'Module pyzipper is not installed')
        return False
    elif 'pyzipper' in sys.modules:
        logging.info(f'Module pyzipper installed')
        return True


def test_zipfile(zfile):
    ''' Test if file is legit Zip file or not '''

    result = zipfile.is_zipfile(zfile)
    return result


def test_read(file):
    ''' Test that file path provided exists and we have read permissions '''

    if os.access(file, os.R_OK):
        return True


def test_exists(file):
    ''' Test that file exists '''
    if os.path.exists(file):
        return True


def extract_file(zfile, password):
    ''' Extract Zip archive given particular password '''

    #print(f'[-] Attempting decryption of {zfile} using password {password}')

    try:
        zfile.extractall(pwd=password.encode("utf-8"))
        print(Fore.GREEN + f"[+] Password found: {password}")
        return (True, password)

    except RuntimeError as runerr:
        print(Fore.LIGHTYELLOW_EX + f'[-] Encountered a runtime error: {runerr}')
        return (False, runerr)

    except Exception as err:
        print(Fore.LIGHTRED_EX + f'[-] Encountered generic exception: {err}')
        return (False, err)


def main():
    ''' Main function '''

    # Check if pyzipper support is present
    result_pyzipper = test_pyzipper()

    if result_pyzipper:
        print(Fore.GREEN + f'[+] You have pyzipper installed, AES encrypted Zip support enabled!')
    if not result_pyzipper:
        print(Fore.LIGHTRED_EX + f'[!] You have not imported the pyzipper module, AES encryption for Zip archives not enabled')

    # Check if file is a Zip file by magic number
    result_zip = test_zipfile(zfile)

    if result_zip:
        print(Fore.GREEN + f'[+] File {zfile} is a valid Zip archive')
    if not result_zip:
        print(Fore.LIGHTRED_EX + f'[!] File {zfile} is not a valid Zip archive, exiting...')
        exit(1)
    
    # Check if file exists
    result_exists = test_exists(zfile)

    if result_exists:
        print(Fore.GREEN + f"[+] File {zfile} exists")
    if not result_exists:
        print(Fore.LIGHTRED_EX + f"[!] File {zfile} doesn't exist")
        exit(1)

    # Check if file can be read
    result_read = test_read(zfile)

    if result_read:
        print(Fore.GREEN + f"[+] File {zfile} is readable")
    if not result_read:
        print(Fore.LIGHTRED_EX + f"[!] File {zfile} cannot be read")
        exit(1)
        
    print(Fore.LIGHTYELLOW_EX + f'[-] Begin extraction subroutine for archive {zfile} with provided password file: {pfile}')

    if result_pyzipper:
        with pyzipper.AESZipFile(zfile) as archive:
            with open(pfile, "r") as dictFile:
                for word in dictFile:

                    password = word.strip("\n")
                    extraction_result = extract_file(archive, password)

                    if extraction_result[0]:
                        print(Fore.GREEN + f'[*] Successfully extracted password-protected Zip archive: {zfile}')
                        break

                    elif not extraction_result[0]:
                        #print(Fore.LIGHTYELLOW_EX + f'[!] Failed to extract password-protected Zip archive: {zfile}')
                        continue

    else:
        with zipfile.ZipFile(zfile) as archive:
            with open(pfile, "r") as dictFile:
                for word in dictFile:

                    password = word.strip("\n")
                    extraction_result = extract_file(archive, password)

                    if extraction_result[0]:
                        print(Fore.GREEN + f'[*] Successfully extracted password-protected Zip archive: {zfile}')
                        break

                    elif not extraction_result[0]:
                        print(Fore.LIGHTYELLOW_EX + f'[!] Failed to extract password-protected Zip archive: {zfile}')

                    if "compress_type=99" in repr(extraction_result[1]):
                        print(Fore.LIGHTRED_EX + f'[!] Fatal error archive {zfile} is AES encrypted and AES encryption support is not present!')
                        exit(1)
                    continue



if __name__ == "__main__":
    main()
