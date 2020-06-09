# author: axi0m
# purpose: rudimentary zip cracker

import zipfile
import argparse
import pyzipper

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


def test_zipfile(zfile):
    ''' Test if file is legit Zip file or not '''
    result = zipfile.is_zipfile(zfile)
    return result


def extractfile(zfile, pfile):
    ''' Attempt to decrypt password protected archive
    
    :param zfile: The zip file to attempt to decrypt
    :param pfile: The password to try
    '''

    print(f'[-] Begin extraction subroutine for archive {zfile} with provided password file: {pfile}')

    with zipfile.ZipFile(zfile) as archive:
        with open(pfile, "r") as dictFile:
            for word in dictFile:
                word = word.strip("\n")

                try:
                    archive.extractall(pwd=word.encode("utf-8"))
                    print(f"[+] Password found: {word}")
                    return (True, word)

                except RuntimeError as runerr:
                    if 'compress_type=99' in repr(runerr):
                        print(f'[!] Zip archive is AES encrypted, cannot use zipfile module to decrypt!')
                        return (False, runerr)
                    else:
                        print(f'[!] Encountered a runtime error: {runerr}')
                        return (False, runerr)

                except Exception as err:
                    print(f'[!] Encountered generic exception: {err}')
                    return (False, err)

def main():
    ''' Main function '''

    # Check if file is a Zip file by magic number
    result = test_zipfile(zfile)

    # Move on to attempt to decrypt and extract the Zip archive
    if result:
        print(f'[+] File {zfile} is a valid Zip archive')
        extraction_result = extractfile(zfile, pfile)
    
    # Let the user know that the file isn't a Zip archive
    else:
        print(f'[!] The file provided is not a Zip file. Please only provide valid Zip files!')
        exit(1)
    
    if extraction_result[0]:
        print(f'[*] Successfully extracted password-protected Zip archive: {zfile}')
        exit(0)
    elif not extraction_result[0]:
        print(f'[!] Failed to extract password-protected Zip archive')
        exit(1)


if __name__ == "__main__":
    main()
