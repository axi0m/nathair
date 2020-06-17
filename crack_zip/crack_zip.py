# author: axi0m
# purpose: rudimentary zip cracker

import argparse
import pyzipper
import zipfile
import sys

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
        return False
    elif 'pyzipper' in sys.modules:
        return True

def test_zipfile(zfile, pyzipper_present):
    ''' Test if file is legit Zip file or not '''

    if pyzipper_present:
        result = pyzipper.zipfile.is_zipfile(zfile)
    else:
        result = zipfile.is_zipfile(zfile)
    
    return result


def extract_file(zfile, password, pyzipper_present):
    ''' Extract Zip archive given particular password '''

    print(f'[+] Attempting decryption of {zfile} using password {password}')

    if pyzipper_present:
        print(f'[+] Pyzipper module installed')

    try:
        zfile.extractall(pwd=password.encode("utf-8"))
        print(f"[+] Password found: {password}")
        return (True, password)

    except RuntimeError as runerr:
        print(f'[-] Encountered a runtime error: {runerr}')
        return (False, runerr)

    except Exception as err:
        print(f'[-] Encountered generic exception: {err}')
        return (False, err)
            

def main():
    ''' Main function '''

    # Check if pyzipper support is present
    result_pyzipper = test_pyzipper()

    if result_pyzipper:
        print(f'[+] You have pyzipper installed, AES encrypted Zip support enabled!')
    else:
        print(f'[!] You have not imported the pyzipper module, AES encryption for Zip archives not enabled')

    # Check if file is a Zip file by magic number
    result = test_zipfile(zfile, result_pyzipper)

    # Move on to attempt to decrypt and extract the Zip archive
    if result:
        print(f'[+] File {zfile} is a valid Zip archive')
        print(f'[+] Begin extraction subroutine for archive {zfile} with provided password file: {pfile}')

        with zipfile.ZipFile(zfile) as archive:
            with open(pfile, "r") as dictFile:
                for word in dictFile:

                    password = word.strip("\n")
                    extraction_result = extract_file(archive, password, result_pyzipper)

                    if extraction_result[0]:
                        print(f'[*] Successfully extracted password-protected Zip archive: {zfile}')
                        break

                    elif not extraction_result[0]:
                        print(f'[!] Failed to extract password-protected Zip archive: {zfile}')

                        if "compress_type=99" in repr(extraction_result[1]):
                            print(f'[!] Fatal error archive {zfile} is AES encrypted and AES encryption support is not present!')
                            exit(1)
                        continue
    
    # Let the user know that the file isn't a Zip archive
    else:
        print(f'[!] The file provided is not a Zip file. Please only provide valid Zip files!')
        exit(1)


if __name__ == "__main__":
    main()
