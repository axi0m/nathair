# author: axi0m
# purpose: rudimentary zip cracker

from zipfile import ZipFile
from zipfile import BadZipFile
import argparse
#import pyzipper

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


def extractfile(zfile, pfile):
    ''' Attempt to decrypt password protected archive 
    
    :param zfile: The zip file to attempt to decrypt
    :param pfile: The password to try
    '''

    print(f'[-] Begin extraction subroutine for archive {zfile} with provided password file: {pfile}')

    with ZipFile(zfile) as archive:
        with open(pfile, "r") as dictFile:
            for word in dictFile:
                word = word.strip("\n")

                try:
                    archive.extractall(pwd=word.encode("utf-8"))
                    print("[+] Password found: {}".format(word))
                    return ("Archive password", word)

                except RuntimeError as runerr:
                    if 'compress_type=99' in repr(runerr):
                        print(f'[!] Zip archive is AES encrypted, cannot use zipfile module to decrypt!')
                        exit(1)
                    else:
                        print(f'[!] Encountered a runtime error: {runerr}')
                        return runerr

                except Exception as err:
                    print(f'[!] Encountered generic exception: {err}')
                    return err


if __name__ == "__main__":
    extractfile(zfile, pfile)
